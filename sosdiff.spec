Name: sosdiff
Version: 0.0.0
Release: py3
Summary: Compare two more sosreports and show the differences.

License: GPLv3
URL:            https://github.com/pafernanr/sosdiff
Source0: https://github.com/pafernanr/%{name}-%{version}.tar.gz
Group: Applications/System
BuildArch: noarch

BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
Compare two more sosreports and show the differences.

%prep
%setup -qn %{name}-%{version}

%build

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tools/sosdiff/bin
install -D -m 755 sosdiff/bin/__init__.py ${RPM_BUILD_ROOT}/usr/lib/tools/sosdiff/bin/__init__.py
cp -rp sosdiff ${RPM_BUILD_ROOT}/usr/lib/tools/

rm -rf ${RPM_BUILD_ROOT}/usr/lib/tools/%{name}/lib/__pycache__

%post
ln -s -f /usr/lib/tools/sosdiff/bin/__init__.py /usr/bin/sosdiff

%postun
if [ $1 -eq 0 ] ; then
    rm -f /usr/bin/%{name}
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
/usr/lib/tools/sosdiff
