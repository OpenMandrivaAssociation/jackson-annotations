Name:		jackson-annotations
Version:	2.21
Release:	1
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
Tests are skipped.

%prep
%setup -q -n jackson-annotations-jackson-annotations-%{version}

%files -f .mfiles
%doc LICENSE README.md SECURITY.md release-notes/VERSION-2.x
