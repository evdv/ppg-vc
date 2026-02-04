# 22kHz
for emotion in confused default enunciated happy sad;
  do
  echo ${emotion};
  # this subfolder was not needed
  # python 1_compute_ctc_att_bnf.py --output_dir /media/emelie/EMELIESSD1/ppgs/expresso_PLA_SP/plain_LJ_NO_VAD/emotion/${emotion}/test/ --wav_dir '/media/emelie/EMELIESSD1/puppeteering/LJ/ARPA/expresso_NO_VAD/no_reference/'${emotion};
  python 1_compute_ctc_att_bnf.py --output_dir /media/emelie/EMELIESSD1/ppgs/expresso_PLA_SP/LJ_MFA_PSOLA2_from_mfa_spk0/emotion/${emotion}/test/ --wav_dir '/media/emelie/EMELIESSD1/puppeteering/LJ_MFA_PSOLA2/ARPA/expresso_NO_VAD/no_reference_spk0/'${emph}
  for speaker in ex01 ex02 ex03 ex04;
    do
      echo ${speaker}
      # python 1_compute_ctc_att_bnf.py --output_dir /media/emelie/EMELIESSD1/ppgs/expresso_PLA_SP/recordings_NO_VAD/emotion/${emotion}/test/ --wav_dir /media/emelie/EMELIESSD1/expresso/audio_22khz/read/${speaker}/${emotion}/base/;
    done;
done;
