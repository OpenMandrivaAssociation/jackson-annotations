Name:		jackson-annotations
Version:	2.23
Release:	2
Summary:	Core annotations for the Jackson data processor
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/FasterXML/jackson-annotations
Source0:	https://github.com/FasterXML/jackson-annotations/archive/refs/tags/jackson-annotations-%{version}.tar.gz#/jackson-annotations-%{version}.tar.gz
# Gradle 9.9.1 strictly pins 2.22 (not 2.22.0). No prebuilt jars.
Source1:	https://github.com/FasterXML/jackson-annotations/archive/refs/tags/jackson-annotations-2.22.tar.gz#/jackson-annotations-2.22.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(com.fasterxml:oss-parent:pom::)
BuildRequires:	mvn(com.fasterxml.jackson:jackson-parent:pom::)
BuildRequires:	fasterxml-oss-parent >= 81
BuildRequires:	jackson-parent >= 2.23
# oss-parent pins the compiler plugin to this ASM jar.
BuildRequires:	mvn(org.ow2.asm:asm)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

Provides:	jackson2-annotations = %{version}-%{release}
Obsoletes:	jackson2-annotations < %{version}-%{release}

%description
Core annotations used by Jackson data binding.
2.23 matches jackson-parent 2.23 and targets Java 8.
Since 2.21 it adds @JsonApplyView, an OptBoolean order property
on @JsonIncludeProperties, JsonTypeInfo.writeTypeIdForDefaultImpl,
and better Locale handling in JsonFormat.Value.
2.23 itself has no annotation changes past 2.22.
2.23 stays the default jar. Gradle 9.9.1 strictly pins 2.22, so
that jar is installed beside it.
The bundle plugin is not packaged, so the jar has no OSGi manifest.
The jar is multi-release: its Java 9 module is
com.fasterxml.jackson.annotation. Tests are skipped.

%prep
%setup -q -n jackson-annotations-jackson-annotations-%{version}
%setup -q -T -D -a 1 -n jackson-annotations-jackson-annotations-%{version}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete

%build -a
mkdir -p target/classes/META-INF/versions/9
javac --release 9 \
	--patch-module com.fasterxml.jackson.annotation=target/classes \
	-d target/classes/META-INF/versions/9 \
	src/moditect/module-info.java
test -s target/classes/META-INF/versions/9/module-info.class
printf 'Multi-Release: true\n' > target/multi-release.mf
jar ufm target/jackson-annotations-%{version}.jar target/multi-release.mf
jar uf target/jackson-annotations-%{version}.jar -C target/classes META-INF/versions/9/module-info.class
java --module-path target/jackson-annotations-%{version}.jar --describe-module com.fasterxml.jackson.annotation | grep -q '^com.fasterxml.jackson.annotation'

export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
mkdir -p ja222/classes
find jackson-annotations-jackson-annotations-2.22/src/main/java -name '*.java' ! -name 'module-info.java' > ja222/sources.list
test -s ja222/sources.list
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-d ja222/classes @ja222/sources.list
"$JAVA_HOME/bin/jar" cf ja222/jackson-annotations.jar -C ja222/classes .
cat > ja222/jackson-annotations.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-annotations</artifactId>
  <version>2.22</version>
  <name>Jackson-annotations</name>
  <description>Core annotations used by Jackson data binding.</description>
  <url>https://github.com/FasterXML/jackson-annotations</url>
  <licenses>
    <license>
      <name>Apache License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF

%install -p
sysjar install --buildroot %{buildroot} \
	--artifact ja222/jackson-annotations.pom:ja222/jackson-annotations.jar \
	--file-name jackson-annotations-2.22 \
	--filelist .mfiles222
# 2.23 owns jackson-annotations.sysjar. 2.22 keeps a second index.
/bin/mv %{buildroot}/usr/share/sysjar/index/com.fasterxml.jackson.core/jackson-annotations.sysjar \
	%{buildroot}/usr/share/sysjar/index/com.fasterxml.jackson.core/jackson-annotations-2.22.sysjar
sed -i 's|/usr/share/sysjar/index/com.fasterxml.jackson.core/jackson-annotations\.sysjar|/usr/share/sysjar/index/com.fasterxml.jackson.core/jackson-annotations-2.22.sysjar|' .mfiles222

%install -a
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles222

%check -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > JaSmoke.java << 'EOF'
import com.fasterxml.jackson.annotation.JsonInclude;
public class JaSmoke {
	public static void main(String[] args) {
		String name = JsonInclude.Include.NON_NULL.name();
		if (!"NON_NULL".equals(name)) {
			throw new AssertionError(name);
		}
		System.out.println(args[0] + " " + name);
	}
}
EOF
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/jackson-annotations.jar JaSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/jackson-annotations.jar:." JaSmoke ja223_ok > check223.log
cat check223.log
grep -F -q 'ja223_ok NON_NULL' check223.log
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/jackson-annotations-2.22.jar JaSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/jackson-annotations-2.22.jar:." JaSmoke ja222_ok > check222.log
cat check222.log
grep -F -q 'ja222_ok NON_NULL' check222.log

%files -f .mfiles
%doc LICENSE README.md SECURITY.md release-notes/VERSION-2.x
