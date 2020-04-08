FROM jupyter/scipy-notebook


RUN pip install elasticsearch



USER $NB_USER

RUN pip install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --user && \
    # can modify or enable additional extensions here
    jupyter nbextension enable spellchecker/main --user


CMD ["start-notebook.sh","--NotebookApp.base_url=/","--NotebookApp.token=''", "--NotebookApp.password=''"]