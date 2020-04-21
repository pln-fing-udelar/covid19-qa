import { Fragment } from "preact";

function FormattedAnswer({ children, answerStartIndex, asnwerEndIndex }) {
  return (
    <Fragment>
      {children.slice(0, answerStartIndex)}
      <b>{children.slice(answerStartIndex, asnwerEndIndex)}</b>
      {children.slice(asnwerEndIndex, children.length)}
    </Fragment>
  );
}

export default FormattedAnswer;
