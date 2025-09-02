Example: 
# CIT
# Input: a.txt, c.bam
# Previous code: initial_code.py
# Annotation: 
# END

Command
python /code/main.py \
    --input_folder /test_file \
    --output_folder /test_output


Intro: Considering that bioinformatics analyses often involve numerous scripts with interdependencies, 
and that multiple versions with different parameters need to be retained simultaneously, a dedicated 
code interdependency tracker is required to construct dependency relationships based on the header 
comments