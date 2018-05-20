python src/init.py 0
python src/project.py status -d -p 1
python src/project.py run
python src/project.py status -d -p 1
python -m jupyter nbconvert --to html --execute src/notebook.ipynb
