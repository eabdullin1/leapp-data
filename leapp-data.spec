%global pes_events_build_date 20240123

%define dist_list almalinux centos eurolinux oraclelinux rocky
%define conflict_dists() %(for i in almalinux centos eurolinux oraclelinux rocky; do if [ "${i}" != "%{dist_name}" ]; then echo -n "leapp-data-${i} "; fi; done)

%if 0%{?rhel} == 7
%if %{dist_name} == "almalinux"
%define gpg_key RPM-GPG-KEY-AlmaLinux-8
%endif
%if %{dist_name} == "centos"
%define gpg_key RPM-GPG-KEY-CentOS-Official
%endif
%if %{dist_name} == "eurolinux"
%define gpg_key RPM-GPG-KEY-eurolinux8
%endif
%if %{dist_name} == "oraclelinux"
%define gpg_key RPM-GPG-KEY-oracle-ol8
%endif
%if %{dist_name} == "rocky"
%define gpg_key RPM-GPG-KEY-Rocky-8
%endif
%endif
%if 0%{?rhel} == 8
%if %{dist_name} == "almalinux"
%define gpg_key RPM-GPG-KEY-AlmaLinux-9
%endif
%if %{dist_name} == "centos"
%define gpg_key RPM-GPG-KEY-CentOS-Official
%endif
%if %{dist_name} == "eurolinux"
%define gpg_key RPM-GPG-KEY-eurolinux9
%endif
%if %{dist_name} == "oraclelinux"
%define gpg_key RPM-GPG-KEY-oracle-ol9
%endif
%if %{dist_name} == "rocky"
%define gpg_key RPM-GPG-KEY-Rocky-9
%endif
%endif

%bcond_without check


Name:		leapp-data-%{dist_name}
Version:	0.2
Release:	7%{?dist}.%{pes-events_build_date}
Summary:	data for migrating tool
Group:		Applications/Databases
License:	ASL 2.0
URL:		https://github.com/AlmaLinux/leapp-data
Source0:	leapp-data-%{version}.tar.gz
BuildArch:  noarch

Conflicts: %{conflict_dists}

%if %{with check}
%if 0%{?rhel} == 7
BuildRequires: python36
BuildRequires: python36-jsonschema
%endif
%if 0%{?rhel} == 8
BuildRequires: python3
BuildRequires: python3-jsonschema
%endif
%endif

%description
%{dist_name} %{summary}


%prep
%setup -q


%build
%if 0%{?rhel} < 8
sh tools/generate_epel_files.sh "%{dist_name}"
%endif


%install
mkdir -p %{buildroot}%{_sysconfdir}/leapp/files/vendors.d
%if 0%{?rhel} < 8
cp -f vendors.d/* %{buildroot}%{_sysconfdir}/leapp/files/vendors.d/
%endif
cp -rf files/%{dist_name}/* %{buildroot}%{_sysconfdir}/leapp/files/


rm -f %{buildroot}%{_sysconfdir}/leapp/files/config.json

%if 0%{?rhel} == 7
mv -f %{buildroot}%{_sysconfdir}/leapp/files/leapp_upgrade_repositories.repo.el8 \
      %{buildroot}%{_sysconfdir}/leapp/files/leapp_upgrade_repositories.repo
mv -f %{buildroot}%{_sysconfdir}/leapp/files/repomap.json.el8 \
      %{buildroot}%{_sysconfdir}/leapp/files/repomap.json
rm -f %{buildroot}%{_sysconfdir}/leapp/files/*.el9
mkdir -p %{buildroot}%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/8/
mv -f files/rpm-gpg/%{gpg_key} %{buildroot}%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/8/
%endif
%if 0%{?rhel} == 8
mv -f %{buildroot}%{_sysconfdir}/leapp/files/leapp_upgrade_repositories.repo.el9 \
      %{buildroot}%{_sysconfdir}/leapp/files/leapp_upgrade_repositories.repo
mv -f %{buildroot}%{_sysconfdir}/leapp/files/repomap.json.el9 \
      %{buildroot}%{_sysconfdir}/leapp/files/repomap.json
rm -f %{buildroot}%{_sysconfdir}/leapp/files/*.el8
mkdir -p %{buildroot}%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/9/
mv -f files/rpm-gpg/%{gpg_key} %{buildroot}%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/9/
%endif

%check
%if %{with check}
JSON_FILES=$(find %{buildroot}%{_sysconfdir}/leapp/ -path "./tests" -prune -o -name "*pes*.json" -print0 | xargs -0 echo)

python3 tests/validate_json.py tests/pes-events-schema.json $JSON_FILES
python3 tests/validate_ids.py $JSON_FILES
python3 tests/check_debranding.py %{buildroot}%{_sysconfdir}/leapp/files/pes-events.json
%endif


%files
%doc LICENSE NOTICE README.md
%if 0%{?rhel} == 8
%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/9/
%endif

%if 0%{?rhel} == 7
%{_sysconfdir}/leapp/repos.d/system_upgrade/common/files/rpm-gpg/8/
%endif
%{_sysconfdir}/leapp/files/*


%changelog
* Mon Feb 05 2024 Eduard Abdullin <eabdullin@almalinux.org> - 0.2-7.20240123
- Add generate_epel_files script to create epel files for EL7
- Add data to support migration from EL7 to EL8 with 
 enabled epel repositories for AlmaLinux-8
- Add pes_events_build_date to spec file to track the pes-events update date

* Tue Jan 16 2024 Eduard Abdullin <eabdullin@almalinux.org> - 0.2-6
- Add gpg keys

* Tue Jan 16 2024 Eduard Abdullin <eabdullin@almalinux.org> - 0.2-5
- Update pes-event file for Rocky, EuroLinux, CentOS Stream, AlmaLinux

* Tue Jan 16 2024 Yuriy Kohut <ykohut@almalinux.org> - 0.2-3.2
- Use YUM archive repo of PostgreSQL 11 for RHEL / Rocky 8 (x86_64)

* Mon Dec 11 2023 Eduard Abdullin <eabdullin@almalinux.org> - 0.2-3.1
- Fix EL8 to EL9 migration

* Mon Mar 27 2023 Andrew Lukoshko <alukoshko@almalinux.org> - 0.2-3
- Add 8 to 9 migration support for Rocky Linux, EuroLinux, CentOS Stream

* Fri Sep 30 2022 Andrew Lukoshko <alukoshko@almalinux.org> - 0.2-2
- Split repomap.json

* Fri Sep 30 2022 Andrew Lukoshko <alukoshko@almalinux.org> - 0.2-1
- Add 8 to 9 migration support for AlmaLinux

* Thu Sep 1 2022 Roman Prilipskii <rprilpskii@cloudlinux.com> - 0.1-7
- made third-party files accessible for all supported distributions

* Wed Aug 17 2022 Andrew Lukoshko <alukoshko@almalinux.org> - 0.1-6
- added repomap.json file for all distributions

* Thu Mar 24 2022 Tomasz Podsiadły <tp@euro-linux.com> - 0.1-5
- Add EuroLinux to supported distributions

* Wed Mar 23 2022 Andrew Lukoshko <alukoshko@almalinux.org> - 0.1-4
- added ResilientStorage and updated repo URLs for AlmaLinux and Rocky

* Thu Oct 21 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 0.1-3
- updated PES data for Oracle and Rocky

* Thu Aug 26 2021 Avi Miller <avi.miller@oracle.com> - 0.1-2
- switched to using the full oraclelinux name
- switched the Oracle Linux repos to use https
- added Apache-2.0 NOTICE attribution file

* Wed Aug 25 2021 Sergey Fokin <sfokin@almalinux.org> - 0.1-1
- initial project
