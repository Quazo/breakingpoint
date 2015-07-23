#!/bin/bash

hip=${1:?"usage: $0 <scene.hip>"}

${HFS:?"Define HFS to your Houdini folder or source the houdini environment."}/bin/hexpand $hip

for init in `find ${hip}.dir -name "*.init"`;
    do sed -ri -e "s/(arnold::[^:]+).+/\1/" $init;
done

$HFS/bin/hcollapse -r $hip
