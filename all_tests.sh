#!/bin/sh

for f in *_test.py
do
  python $f
done

#python server_load_balancer_test.py
#python server_test.py
#python parser_test.py
