if [ -e "drill/user/__g" ]; then
  mv drill/user/__g .
fi

rm -fr drill
tar zxvf drill.tar.gz

if [ -e "./__g" ]; then
    mv ./__g drill/user/
else
    rm drill/user/__g
fi

sudo /etc/init.d/apache2 restart

