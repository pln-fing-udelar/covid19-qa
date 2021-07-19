export const UnrelatedParagraphFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    No está relacionado con la pregunta.
  </button>
);

export const RelatedParagraphFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    Está relacionado pero no contiene la respuesta.
  </button>
);

export const GoodParagraphFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    Contiene la respuesta.
  </button>
);

export const ExactMatchFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    Coincide exactamente con la respuesta.
  </button>
);

export const ContainedMatchFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    Contiene la respuesta.
  </button>
);

export const IncompleteMatchFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    Contiene parte de la respuesta.
  </button>
);

export const NoMatchFeedbackButton = (props) => (
  <button class="p-1 hover:text-gray-600" border="none" background-color="inherit" {...props}>
    No contiene nada de la respuesta.
  </button>
);