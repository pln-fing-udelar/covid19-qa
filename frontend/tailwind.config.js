module.exports = {
  theme: {
    extend: {
      minWidth: {
        "1/4": "25%",
        "1/2": "50%",
        "3/4": "75%",
      },
      transitionProperty: {
        height: "height",
      },
    },
  },
  variants: { margin: ["last", "responsive"] },
  plugins: [],
};
