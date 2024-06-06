#out/Bytecode/chrome $URL --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/testpath --no-crankshaft --no-turbo --no-ignition" --no-sandbox --disable-hang-monitor -enable-nacl&>log_file

#usage: sudo bash validate-nonxss-phase3.sh 386560 1000000 2 16 0 2>&1 | grep -vE "Xlib:  extension \"RANDR\" missing on display \".*\"\.|Xlib:  extension \"XInputExtension\" missing on display \".*\"\.|ERROR:zygote_communication_linux.cc\(292\)\] Failed to" | tee -a ./detector_phase3_db_crawling.log

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/media/data1/zfk/Documents/capnproto-install/lib
# export SAVE_PATH=/home/zfk/Documents/sanchecker
export SAVE_PATH=/media/datak/inactive/sanchecker # /media/data1/zfk/Documents/sanchecker

### Important: 1-177773 are under ~/.../, 177773-- are under /media/data1/.../

start_line=$1
end_line=$2
if_flush=$3 # 1 for flush in path TAG="", 0 for flush in path TAG=<self_defined>, other for not flush
#sleep_time=$4
max_num_window=$4
if_clear_taint_log_files=$5 # 1 for not using taint log files

rm -rf ~/.cache/chromium ~/.config/chromium
find /tmp/ -mindepth 1 -maxdepth 1 ! -name 'ssh-*' ! -name 'systemd*' ! -name 'mongodb-*' -exec rm -rf {} +

# rm -rf /tmp/*_com* /tmp/*_net /tmp/*_org /tmp/*_io /tmp/*_edu* /tmp/*cn /tmp/*_uk /tmp/*_fr /tmp/*jp /tmp/*gov /tmp/google* /tmp/zo* /tmp/www* /tmp/*co /tmp/*ir
cd ${SAVE_PATH}/src
if ((if_flush == 1))
then
        rm -rf ../crawl && mkdir ../crawl
        rm -rf logs && mkdir logs
        TAG=""
else
        TAG="validate_nonxss_phase3_db_"
	if ((if_flush == 0))
        then
                rm -rf ../${TAG}crawl && mkdir ../${TAG}crawl && chmod 777 ../${TAG}crawl
                rm -rf ${TAG}logs && mkdir ${TAG}logs && chmod 777 ${TAG}logs
	else
		mkdir -p ../${TAG}crawl && chmod 777 ../${TAG}crawl
                mkdir -p ${TAG}logs && chmod 777 ${TAG}logs
	fi
        
fi

cd /media/data1/zfk/Documents/sanchecker/src

while IFS=, read -r idx url
do
    if (( idx > $start_line && idx <= $end_line ))
    then
            url="${url//[$'\t\r\n ']}" #remove newline from string
            # Skip URLs ending with ".pl"
                if [[ "$url" == *".pl" ]]
                then
                        continue
                fi
            NAME="${url/./_}"
            rm -rf /tmp/${NAME}
            echo "${idx} ${url} ${TAG}logs, ${NAME}" #_log_file sanchecker/${TAG}crawl/$NAME"
            out/Oracle-release/chrome ${url} --js-flags="--taint_log_file=${SAVE_PATH}/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition --phase3_enable --current_site=${url}" \
                     --user-data-dir=/tmp/${NAME} --load-extension=/home/zfk/Documents/crawler-extension,/home/zfk/Documents/validate_pp_extension --new-window --no-sandbox --disable-gpu --disable-hang-monitor --ignore-certificate-errors --allow-insecure-localhost &>${SAVE_PATH}/src/${TAG}logs/${NAME}_log_file & #& pkill chrome > /dev/null &  #&>logs/${NAME}_log_file &
#sudo out/Oracle-release/chrome https://www.mountvernon.org/?K1.K2=V --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/testdir/mountvernon_org --phase3_enable --current_site=mountvernon.org --no-crankshaft --no-turbo" --user-data-dir=/tmp/test_chromium --load-extension=/home/zfk/Documents/inject_pp_extension/ --new-window --no-sandbox --disable-hang-monitor --disable-gpu --ignore-certificate-errors --allow-insecure-localhost > /home/zfk/temp/phase3_release_db_mountvernon_org_log_file

            if (( (idx - ($start_line)) % $max_num_window == 0 ))
            then
                    echo "Waiting to clean $idx and prev $max_num_window windows ... "
                    # timeout 60 out/Bytecode/chrome $url --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition" \
                    # --new-window --no-sandbox --disable-hang-monitor -incognito -enable-nacl &>${TAG}logs/${NAME}_log_file && pkill chrome
                    sleep 45s
                    pkill chrome
			pkill chrome                    
			sleep 1s
                    echo "$idx and prev $max_num_window windows cleaned! "
                    # remove user-data in /tmp/ ; remove useless downloaded files; drop caches
		    find /tmp/ -mindepth 1 -maxdepth 1 ! -name 'ssh-*' ! -name 'systemd*' ! -name 'mongodb-*' -exec rm -rf {} +
			# When not using taint log files in the crawl/
                    if (( if_clear_taint_log_files == 1))
                    then
                        rm -rf ${SAVE_PATH}/${TAG}crawl/*
                    fi
		            rm -rf /home/zfk/Downloads/*
                    sync; sh -c "echo 1 > /proc/sys/vm/drop_caches"
                    cd /media/data1/zfk/Documents/sanchecker/src
		#     rm -rf /tmp/*_com /tmp/*_net /tmp/*_org /tmp/*_io /tmp/*_edu* /tmp/*_cn /tmp/*_uk
                
            #else
                    
            fi
            #sleep ${sleep_time}s --user-data-dir=/tmp
    elif ((idx > $end_line))
    then
            echo "Come to the end $idx. Waiting to clean all windows ... "
            sleep 80s
            pkill chrome
            echo "All windows cleaned!"
            #echo "Finished and keep the windows to see if anything killed ... "
	    break
    fi
# Note: the current tranco_3Z3L.csv gets rid of websites with domain '.pl'
# The bash cmd is: sudo sed -i.old '/.*\.pl/d' tranco_3Z3L.csv
done < <(grep . /media/datak/inactive/analysis/phase3/nonxss_sink_to_validate_website_list.csv ) #tranco_253N9-1m.csv) #websites_total_to_pp_pattern1_600kto1m.txt) #42_websites_url_src_to_pp_again_0to600kplus.txt)  #websites_total_to_pp_pattern1_0to600kplus.txt #websites_to_pp_pattern1_0to200k.txt
#/media/data1/zfk/Documents/sanchecker/src/recursive_pp_pattern1_rankmorethan10k_logs/websites_to_pp.txt #tranco_94Q2.csv
sleep 80s
pkill chrome
echo "All windows cleaned!"
# Previous unsuccessful cmd FYI
#export FILE="./logs/${NAME}_log_file"
            #echo "logs/${NAME}_log_file"
            #CMD="out/Bytecode/chrome $url --js-flags=\"--taint_log_file=/media/data1/zfk/Documents/sanchecker/crawl/$NAME --no-crankshaft --no-turbo --no-ignition\" --no-sandbox --disable-hang-monitor -incognito -enable-nacl&>${NAME}_log_file"

#echo $CMD
            #bash -c $CMD
            #screen -S $idx -dm bash -c $CMD
