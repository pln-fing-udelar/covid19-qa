const { parsed } = require("dotenv").config();

module.exports = (config, env, helpers) => {
  if (env.dev) {
    config.devServer.proxy = [
      {
        path: "/api/**",
        target: "http://localhost:8000",
      },
    ];
  }

  const { plugin: definePlugin } = helpers.getPluginsByName(
    config,
    "DefinePlugin"
  )[0];

  for (const key of Object.keys(parsed)) {
    definePlugin.definitions[`process.env.PREACT_APP_${key}`] = JSON.stringify(
      parsed[key]
    );
  }
  console.log(definePlugin.definitions);
  const postCssLoaders = helpers.getLoadersByName(config, "postcss-loader");
  postCssLoaders.forEach(({ loader }) => {
    const plugins = loader.options.plugins;

    // Add tailwind css at the top.
    plugins.unshift(require("tailwindcss"));
  });
  return config;
};
