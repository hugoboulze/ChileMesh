#!/bin/bash -e
cat <<EOF
The following are necessary, let's try to detect them:
- gmt (6.3.0+)
- python (including numpy, matplotlib)
- Zset, including:
  - python interface
  - MMG interface
EOF

echo "** gmt **"
type gmt && { gmt="ok" ; } || { gmt="ko (not found)"; }
# if dpkg available, use it to check that the version is good enough:
if type dpkg 2>/dev/null; then
    if dpkg --compare-versions $(gmt --version) lt 6.3.0; then
	gmt="$gmt (version $(gmt --version) < 6.3.0)"
    fi
fi


echo "** python **"
type python3
python3 -c "import numpy; print('numpy is here')"
python3 -c "import matplotlib; print('matplotlib is here')"
python3 -c "import matplotlib, numpy" && { py=ok; } || { py=ko; }

echo "** Zset **"
type Zrun && { z=ok ; } || { z=ko ; }
echo "** Zset's python"
python3 -m zset && { zpy=ok ; } || { zpy=ko ; }
echo "** Zset's MMG**"
type $Z7PATH/PUBLIC/lib-Linux_64/libZMMG.so && { zmmg=ok ; } || { zmmg=ko ; }


check_zcracks_version() {
    # ./Zcracks_base.z7p is only needed in Zrun --version < 23097
    cat <<EOF | python3
import os.path
import zset
v = int(zset.version.svn_revision)
if v < 23097:
  exit(1)
EOF
}
echo "** Zcracks's version"
check_zcracks_version && { zcracks=ok; } || { zcracks="ko (version<23097)"; }


cat <<EOF

** Summary **
gmt     is $gmt
python  is $py
Zset    is $z
Zpy     is $zpy
Zcracks is $zcracks
Zmmg    is $zmmg
EOF


