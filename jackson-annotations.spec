%_javapackages_macros
Name:          jackson-annotations
Version:       2.2.2
Release:       3.0%{?dist}
Summary:       Core annotations for Jackson data processor 
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonHome
Source0:       https://github.com/FasterXML/jackson-annotations/archive/%{name}-%{version}.tar.gz
# jackson-annotations package don't include the license file
# https://github.com/FasterXML/jackson-annotations/issues/14
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: mvn(com.fasterxml:oss-parent) >= 10
BuildRequires: java-devel

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-plugin-bundle
BuildRequires: maven-site-plugin

Provides:      jackson2-annotations = %{version}-%{release}
Obsoletes:     jackson2-annotations < %{version}-%{release}

BuildArch:     noarch

%description
Core annotations used for value types,
used by Jackson data-binding package.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

%build

%mvn_file : %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt README.md release-notes/*

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-annotations

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-annotations

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm