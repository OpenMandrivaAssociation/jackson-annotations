Name:		jackson-annotations
Version:	2.21
Release:	2
Summary:	Core annotations for the Jackson data processor
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/FasterXML/jackson-annotations
Source0:	https://github.com/FasterXML/jackson-annotations/archive/refs/tags/jackson-annotations-%{version}.tar.gz#/jackson-annotations-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(com.fasterxml:oss-parent:pom::)
BuildRequires:	mvn(com.fasterxml.jackson:jackson-parent:pom::)
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
2.21 matches jackson-parent 2.21 and targets Java 8.
It adds JsonInclude.Value constants, @JsonDeserializeAs,
@JsonSerializeAs, a radix property on @JsonFormat, and
JsonTypeInfo.As.NOTHING.
The bundle plugin is not packaged, so the jar has no OSGi manifest.
The jar is multi-release: its Java 9 module is
com.fasterxml.jackson.annotation. Tests are skipped.

%prep
%setup -q -n jackson-annotations-jackson-annotations-%{version}

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

%files -f .mfiles
%doc LICENSE README.md SECURITY.md release-notes/VERSION-2.x
