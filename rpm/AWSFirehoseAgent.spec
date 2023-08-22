Name:           aws-kinesis-agent
Version:        2.0.6
Release:        1e%{?dist}
Summary:        Amazon Kinesis Streaming Data Agent

Group:          Applications/Communications
License:        Amazon Software License and Apache 2.0 and MIT
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:            http://aws.amazon.com/

BuildRequires:  ant
BuildRequires:  java-1.8.0-amazon-corretto-devel
Requires:       java >= 1:1.8.0
Provides:       bundled(Slf4j) = 1.7
Provides:       bundled(JakartaCommons-lang3) = 3.4
Provides:       bundled(JCommander) = 1.48
Provides:       bundled(SQLiteJDBC) = 3.8.11
Provides:       bundled(AWSJavaSDKExternalRelease) = 1.10

%global daemon_name aws-kinesis-agent
%global agent_user_name aws-kinesis-agent-user
%global aws_sdk_version 1.11.700
%global config_dir %{_sysconfdir}/aws-kinesis
%global config_flow_dir %{config_dir}/agent.d
%global jar_dir %{_datadir}/%{daemon_name}/lib

%if 0%{?_initddir:1}
%global init_dir %{_initddir}
%else
%global init_dir %{_initrddir}
%endif

%global cron_dir %{_sysconfdir}/cron.d
%global sysconfig_dir %{_sysconfdir}/sysconfig
%global log_dir %{_localstatedir}/log/%{daemon_name}
%global state_dir %{_localstatedir}/run/%{daemon_name}

%description
aws-kinesis-agent is a software service that runs on customer hosts and continuously monitors a set of log files 
and sends new data to the Amazon Kinesis Stream service and Amazon Kinesis Firehose service in near-real-time.

%prep
cd %{_topdir}/BUILD
sudo rm -rf %{name}
mkdir %{name}
cp -rf %{_topdir}/SOURCES/%{name}/* %{name}
%setup -D -T -n %{name}

%build
sudo ./setup --build
sudo chown -R builder:builder .

%install
rm -rf %{buildroot}
install -d %{buildroot}
install -d %{buildroot}%{config_dir}
install -d %{buildroot}%{config_flow_dir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{jar_dir}
install -d %{buildroot}%{init_dir}
install -d %{buildroot}%{cron_dir}
install -d %{buildroot}%{sysconfig_dir}
install -d %{buildroot}%{log_dir}
install -d %{buildroot}%{state_dir}
install -m755 ./bin/start-%{daemon_name} %{buildroot}%{_bindir}
install -m755 ./bin/%{daemon_name}-babysit %{buildroot}%{_bindir}
install -m644 ./dependencies/* %{buildroot}%{jar_dir}
rm %{buildroot}%{jar_dir}/lombok*
install -m644 ./ant_build/lib/* %{buildroot}%{jar_dir}
install -m644 ./configuration/release/%{daemon_name}.json %{buildroot}%{config_dir}/agent.json
install -m755 ./bin/%{daemon_name}.RedHat %{buildroot}%{init_dir}/%{daemon_name}
install -m644 ./support/%{daemon_name}.cron %{buildroot}%{cron_dir}/%{daemon_name}
install -m644 ./support/%{daemon_name}.sysconfig %{buildroot}%{sysconfig_dir}/%{daemon_name}
install -m644 ./support/log4j.xml %{buildroot}%{config_dir}/log4j.xml

%pre
# Add the "agent" user
/usr/sbin/useradd -c "Streaming Data Agent" \
	-s /sbin/nologin -r -d %{_datadir}/%{daemon_name} %{agent_user_name} 2> /dev/null || :

%post
# Initial installation
/sbin/chkconfig --add %{name}
  
%preun
if [ $1 -eq 0 ] ; then
    # Package remove, not upgrade
    /sbin/service %{name} stop >/dev/null 2>&1 ||:
    /sbin/chkconfig --del %{name} ||:
fi
  
%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service %{name} condrestart >/dev/null 2>&1 ||:
fi

%clean
rm -rf %{buildroot}

%files
%doc LICENSE.txt
%doc NOTICE.txt
%doc README.md
%dir %{_datadir}/%{daemon_name}
%dir %{config_dir}
%dir %{config_flow_dir}
%config(noreplace) %{config_dir}/agent.json
%config(noreplace) %{config_dir}/log4j.xml
%config(noreplace) %{sysconfig_dir}/%{daemon_name}
%{init_dir}/%{daemon_name}
%{cron_dir}/%{daemon_name}
%{_bindir}/start-%{daemon_name}
%{_bindir}/%{daemon_name}-babysit
%dir %{jar_dir}
%{jar_dir}/AWSKinesisStreamingDataAgent-1.1.jar
%{jar_dir}/aws-java-sdk-cloudwatch-%{aws_sdk_version}.jar
%{jar_dir}/aws-java-sdk-core-%{aws_sdk_version}.jar
%{jar_dir}/aws-java-sdk-kinesis-%{aws_sdk_version}.jar
%{jar_dir}/aws-java-sdk-sts-%{aws_sdk_version}.jar
%{jar_dir}/aws-java-sdk-ec2-%{aws_sdk_version}.jar
%{jar_dir}/commons-cli-1.2.jar
%{jar_dir}/commons-codec-1.15.jar
%{jar_dir}/commons-lang3-3.4.jar
%{jar_dir}/commons-logging-adapters-1.1.jar
%{jar_dir}/commons-logging-api-1.1.jar
%{jar_dir}/guava-31.1-jre.jar
%{jar_dir}/httpclient-4.5.13.jar
%{jar_dir}/httpclient-cache-4.5.1.jar
%{jar_dir}/httpcore-4.4.3.jar
%{jar_dir}/httpcore-ab-4.4.3.jar
%{jar_dir}/httpcore-nio-4.4.3.jar
%{jar_dir}/httpmime-4.5.1.jar
%{jar_dir}/jackson-annotations-2.14.2.jar
%{jar_dir}/jackson-core-2.14.2.jar
%{jar_dir}/jackson-databind-2.14.2.jar
%{jar_dir}/jackson-dataformat-cbor-2.14.2.jar
%{jar_dir}/jackson-dataformat-xml-2.14.2.jar
%{jar_dir}/jcommander-1.82.jar
%{jar_dir}/joda-time-2.8.2.jar
%{jar_dir}/jsr305-3.0.1.jar
%{jar_dir}/slf4j-api-1.7.12.jar
%{jar_dir}/log4j-api-2.17.1.jar
%{jar_dir}/log4j-core-2.17.1.jar
%{jar_dir}/log4j-slf4j-impl-2.17.1.jar
%{jar_dir}/log4j-1.2-api-2.17.1.jar

%{jar_dir}/sqlite-jdbc-3.42.0.0.jar
%attr(0755,%{agent_user_name},%{agent_user_name}) %dir %{log_dir}
%attr(0755,%{agent_user_name},%{agent_user_name}) %dir %{state_dir}

%changelog
* Tue Jun 21 2022 Mike Patnode <mike.patnode@britive.com> - 2.0.6-1c
- Bumped commons-codec to 1.15

* Tue Apr 21 2022 Mike Patnode <mike.patnode@britive.com> - 2.0.6-1b
- Bumped fasterXML to 2.13.2
- Bumped guava to 31.1
- Bumped jcommander to 1.82

* Mon Jan 6 2022 Marat Khusainov <khumarat@amazon.com> - 2.0.6
- Bumped log4 version to 2.17.1

* Mon Dec 20 2021 Marat Khusainov <khumarat@amazon.com> - 2.0.5
- Bumped log4 version to 2.17.0

* Tue Dec 14 2021 Marat Khusainov <khumarat@amazon.com> - 2.0.4
- Bumped log4 version to 2.16.0

* Fri Dec 10 2021 Marat Khusainov <khumarat@amazon.com> - 2.0.3
- Bumped log4 version to 2.15.0

* Fri Mar 19 2021 Marat Khusainov <khumarat@amazon.com> - 2.0.2
- Bumped jackson-databind version to 2.10.5

* Thu Aug 27 2020 Marat Khusainov <khumarat@amazon.com> - 2.0.1
- Fix for rolling log4j log 

* Thu Jul 16 2020 Yiyang Gong <yiyagong@amazon.com> - 2.0.0-1
- Require Java 1.8
- Switch Guava 28.2-android to 28.2-jre
- Update log4j version to 2.13.2

* Tue Jun 23 2020 Marat Khusainov <khumarat@amazon.com> - 1.1.6-1
- Updated Guava 18 to 28.2-android to address security issue at 
- https://www.cvedetails.com/vulnerability-list/vendor_id-1224/product_id-52274/opdos-1/Google-Guava.html
- and keep jdk7

* Fri Apr 23 2020 Marat Khusainov <khumarat@amazon.com> - 1.1.5-1
- Upgrade Log4j loggers to 2.x
- Upgrade aws sdk version to 1.11.700
- Upgrade jackson api version to 2.10.3

* Fri Dec 13 2019 Chaochen Qian <chaocheq@amazon.com> - 1.1.4-1
- Allow users to add their customized credential provider to use Amazon Kinesis Agent
- Fix the checkpoint position where there remains incomplete record in currentBuffer
- Preserve the multi-line record if it's broken in the middle of the line
- Add notrim,escape_new_line to singleline mode
- Add pluggable data converter
- Add optional timestamp argument to AddMetadataConverter
- Replace the internal custom logger with Log4j standard loggers

* Fri Dec 16 2017 Chaochen Qian <chaocheq@amazon.com> - 1.1.3-1
- Add fileFooterPattern to give up tailing if not necessary
- Add separate config directory for flow configurations
- Add Ec2 metadata processor
- Fix a bug in checkpointing when pre-processing is enabled
- Add AggregationSplitter which enables record aggregation
- Allow CW metrics to include instance tag	
- Add a new pre-processor for addition of arbitrary metadata in JSON format
- Minor fix in logging and exception handling

* Thu Sep 07 2016 Chaochen Qian <chaocheq@amazon.com> - 1.1.2-1
- Add support to use IAM role in Kinesis/Firehose client
- Fix race condition in babysitter

* Thu Jul 14 2016 Chaochen Qian <chaocheq@amazon.com> - 1.1-1
- Bug fixes
- Merge from Github repo

* Wed Mar 23 2016 Chaochen Qian <chaocheq@amazon.com> - 1.1-0
- Add data processing capabilities

* Tue Sep 22 2015 Chaochen Qian <chaocheq@amazon.com> - 1.0-0
- Initial release
