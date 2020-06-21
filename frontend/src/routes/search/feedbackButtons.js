export const PositiveFeedbackButton = (props) => (
  <button name="Sí" title="Sí" class="p-1 hover:text-gray-600" {...props}>
    <svg
      aria-hidden
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      class="h-4 w-4 fill-current"
    >
      <path d="M11 0h1v3l3 7v8a2 2 0 0 1-2 2H5c-1.1 0-2.31-.84-2.7-1.88L0 12v-2a2 2 0 0 1 2-2h7V2a2 2 0 0 1 2-2zm6 10h3v10h-3V10z" />
    </svg>
  </button>
);

export const NegativeFeedbackButton = (props) => (
  <button name="No" title="No" class="p-1 hover:text-gray-600" {...props}>
    <svg
      aria-hidden
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      class="h-4 w-4 fill-current"
    >
      <path d="M11 20a2 2 0 0 1-2-2v-6H2a2 2 0 0 1-2-2V8l2.3-6.12A3.11 3.11 0 0 1 5 0h8a2 2 0 0 1 2 2v8l-3 7v3h-1zm6-10V0h3v10h-3z" />
    </svg>
  </button>
);

export const PartialFeedbackButton = (props) => (
  <button name="Parcial" title="Parcial" class="p-1 hover:text-gray-600" {...props}>
    <svg
      aria-hidden
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      class="h-4 w-4 fill-current"
    >
      <path d="M11 0h1v3l3 7v8a2 2 0 0 1-2 2H5c-1.1 0-2.31-.84-2.7-1.88L0 12v-2a2 2 0 0 1 2-2h7V2a2 2 0 0 1 2-2zm6 10h3v10h-3V10z" />
    </svg>
  </button>
);

export const ReportButton = (props) => (
  <button
    name="Denunciar"
    title="Denunciar"
    class="p-1 hover:text-gray-600"
    {...props}
  >
    <svg
      aria-hidden
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      class="h-4 w-4 fill-current"
    >
      <path d="M7.667 12H2v8H0V0h12l.333 2H20l-3 6 3 6H8l-.333-2z" />
    </svg>
  </button>
);
