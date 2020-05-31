// This fetch wrapper is based in: https://github.com/kentcdodds/bookshelf

async function client(endpoint, { body, ...customConfig } = {}) {
  const headers = { "Content-Type": "application/json" };

  const config = {
    method: body ? "POST" : "GET",
    ...customConfig,
    headers: {
      ...headers,
      ...customConfig.headers,
    },
  };
  if (body) {
    config.body = JSON.stringify(body);
  }

  return window
    .fetch(`${process.env.PREACT_APP_API_URL}/${endpoint}`, config)
    .then(async (r) => {
      if (r.status === 204) {
        // avoid an exception trying to parse an empty response
        return {};
      }

      const data = await r.json();
      if (r.ok) {
        return data;
      } else {
        return Promise.reject(data);
      }
    });
}

const getFAQ = () => client("frequent-questions");

const postFeedback = (answerId, feedback) => client("feedback/", {body: {feedback, answer_id: answerId}});

const search = question => client("question/", {body: {question}})
    .then(answers => {
        answers = answers.map(a => {
            a.prob = Math.round(parseFloat(a.prob) * 100);
            a.logit = parseFloat(a.logit);
            return a;
        })
        answers.sort((a1, a2) => a2.prob - a1.prob);  // They're compared rounded, but it doesn't matter.
        return answers.filter((a) => (a.prob >= 10));
    });

export { getFAQ, postFeedback, search };
