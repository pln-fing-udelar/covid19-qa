FROM jupyter/scipy-notebook


RUN pip install elasticsearch



USER $NB_USER

RUN pip install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --user && \
    # can modify or enable additional extensions here
    jupyter nbextension enable spellchecker/main --user


CMD ["start-notebook.sh","--NotebookApp.base_url=/","--NotebookApp.password='sha1:94fe51d458ce:e0d335f16d95a88e453ae748eb161b5cbe2ffbaa'"]