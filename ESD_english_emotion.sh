# 16kHz
# check 1_compute_ctc_att_bnf.py (SAMPLE_RATE, line 17)
# check config.yaml (lines 185-187, fs 16000)
# ESD recordings, 4-5 fail for each emotion category

#for emotion in Angry Sad Neutral Happy Surprise;
#do echo ${emotion};
#  for subset in 'test';
#do python 1_compute_ctc_att_bnf.py --output_dir /media/emelie/EMELIESSD1/ppgs/ESD_PLA_SP/recordings_NO_VAD/emotion/${emotion}/${subset}/ --wav_dir /media/emelie/EMELIESSD1/Emotional_Speech_Dataset_\(ESD\)/English/${emotion}/${subset}/;
#done;
#done

# 22kHz
for emotion in Angry Sad Neutral Happy Surprise;
do echo ${emotion};
  # this subfolder was not needed
  for subset in 'test';
do python 1_compute_ctc_att_bnf.py --output_dir /media/emelie/EMELIESSD1/ppgs/ESD_PLA_SP/plain_LJ_NO_VAD/emotion/${emotion}/${subset}/ --wav_dir /media/emelie/EMELIESSD1/puppeteering/LJ/ARPA/ESD_NO_VAD/no_reference/${emotion}/;
done;
done
