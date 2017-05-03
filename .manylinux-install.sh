#!/usr/bin/env bash

set -e -x

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    if [[ "${PYBIN}" == *"cp27"* ]] || [[ "${PYBIN}" == *"cp34"* ]] || [[ "${PYBIN}" == *"cp35"* ]]; then
        "${PYBIN}/pip" install -r /io/requirements.txt
        "${PYBIN}/pip" install coveralls
        "${PYBIN}/pip" install -e /io/
        "${PYBIN}/parserator" train training/labeled.xml usaddress
        "${PYBIN}/pip" wheel /io/ -w wheelhouse/
    fi
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/usaddress*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    if [[ "${PYBIN}" == *"cp27"* ]] || [[ "${PYBIN}" == *"cp34"* ]] || [[ "${PYBIN}" == *"cp35"* ]]; then
        "${PYBIN}/pip" uninstall -y usaddress
        "${PYBIN}/pip" install usaddress --no-index -f /io/wheelhouse
        cd /io/
        "${PYBIN}/nosetests" tests --with-coverage --cover-package=usaddress
        cd /
    fi
done

# If everything works, upload wheels to PyPi
tagged=$( cat /io/.travis_tag )
PYBIN34="/opt/python/cp34-cp34m/bin"
if [[ $tagged ]]; then
    "${PYBIN34}/pip" install twine;
    "${PYBIN34}/twine" upload --config-file /io/.pypirc /io/wheelhouse/usaddress*.whl;
fi
