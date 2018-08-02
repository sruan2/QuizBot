## Data file setup

Download files from https://drive.google.com/drive/u/0/folders/1kyEVRudlOC2dxvJSeYztT9-YHpeCgAUo

Move the `mittens_model.pkl` and `glove.6B.100d.pkl` files into the data_files folder 

## Creating the mittens model

If wanting to create the `mitten_model.pkl` from scratch:

1: Install dependencies (`glove` and `mitten`) packages:
https://github.com/roamanalytics/mittens
https://github.com/maciejkula/glove-python

2: run `python build_glove_cooccurrence` to create `data_files/weighted_matrix.pkl` and `data_files/vocab.pkl` files
If wanting to train own corpus, can replace the `data_files/science_corpus` file with different space delimitered file

3: `python mittens_model.py` after putting in the `glove.6B.100d.pkl` file in the correct folder to create `mittens_model.pkl`

## Creating relatedness scores csv
1: `cd data_files`
2: `python generate_csv.py
Edit the list of lists in the file if wanting to include additional 

## Fit the semi-supervised model 
1: `python supervised_model.py`
saves the weights and architecture to the `data_files` folder to be loaded by model
