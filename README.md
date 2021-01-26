We are given an audio which is a periodic signal comprising stick beating sound, and the human voice (called 
as bols/syllables). There were no musical instruments used. We need to recognize and classify the audio.

Code Flow and Code Files explained:-

-> The first step is to remove the silence beats, make the audio into chunks of music and classify it into Stick Beats,
Audio Bols, Audio Bols along with stick beats. We use frequency for that classification. This is done in 
stick_beats_seperator.py. Root director should be set according to the location of our data.

-> We use the get_frequency() function in freq_calculator.py to get the average frequency of a chunk

-> Now we evaluate our segmentation with the correct segmentation, using segmentation_evaluator.py

-> So, we have segmented the audio into Bols, now the next target is to recognize them. We would use Support Vector 
Machine algorithm for it.

-> Before using ML algorithm on the audio, we need to extract features. We would use the MFCC features. We extract the 
features and store them in Excel files so that we need to do it every time for applying a new ML model. It is done in
feature_extractor.py

-> Now we train the model and test it in bol_recognition.py. It also displays the heat map of confusion matrix.