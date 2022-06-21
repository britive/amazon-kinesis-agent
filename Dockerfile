FROM amazoncorretto:8

RUN yum install -y ant \
                   java-1.8.0-amazon-corretto-devel \
                   which \
                   git \
                   pkgconfig \
                   sudo \
                   automake autoconf \
                   yum-utils rpm-build && \
    yum clean all

RUN useradd builder -u 1000 -m -G users,wheel && \
    echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "%_topdir    /home/builder/rpm" >> /home/builder/.rpmmacros && \
    mkdir -p /home/builder/rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    chown -R builder /home/builder
USER builder

ENV FLAVOR=rpmbuild OS=centos DIST=el7
