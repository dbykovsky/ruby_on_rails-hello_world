FROM ruby:2.4-stretch
RUN apt-get update \
    && apt-get install -y nodejs
WORKDIR /workspace/
COPY Gemfile* ./
RUN bundle install
COPY . .
