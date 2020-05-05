FROM node:13-buster

WORKDIR /usr/src/app

COPY *.json *.js ./
RUN npm install

COPY src ./src

EXPOSE 8080

ARG api_url="http://api:8000"
RUN echo -e "API_URL=/api\nDEV_PROXY_TARGET=$api_url" > .env

ARG app_env=development
ENV NODE_ENV $app_env

# The thing is that NODE_ENV (and the API URL) is set at *build* time.
# So we need to do some tricks to work well on production and development.
# For now, we build at container run time, and just run the web dev server always
# (using whatever app_env value is input).

CMD npm run dev
#CMD if [ ${NODE_ENV} = production ]; then \
#    npm install -g http-server && \
#    npm run build && \
#    cd build && \
#    hs -p 8080; \
#	else \
#	  npm run dev; \
#	fi
