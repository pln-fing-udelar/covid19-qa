import { Fragment } from "preact";
import { useState } from "preact/hooks";
import {
  PositiveFeedbackButton,
  NegativeFeedbackButton,
  ReportButton,
} from "./feedbackButtons";
import feedbackChoices from "./feedbackChoices";
import { postFeedback } from "../../utils/api-client";

export default function FeedbackSection({ answerId }) {
  const [feedbackSubmissionStatus, setFeedbackSubmissionStatus] = useState(
    "idle"
  );

  const onFeedbackSubmit = (answerId, feedbackChoice) => {
    setFeedbackSubmissionStatus("loading");
    postFeedback(answerId, feedbackChoice)
      .then(() => setFeedbackSubmissionStatus("success"))
      .catch(() => {
        setFeedbackSubmissionStatus("error");
      });
  };
  if (feedbackSubmissionStatus === "idle") {
    return (
      <Fragment>
        <span class="mr-3">¿Te resultó útil?</span>
        <PositiveFeedbackButton
          onClick={() => onFeedbackSubmit(answerId, feedbackChoices.positive)}
        />

        <NegativeFeedbackButton
          onClick={() => onFeedbackSubmit(answerId, feedbackChoices.negative)}
        />
        <ReportButton
          onClick={() => onFeedbackSubmit(answerId, feedbackChoices.report)}
        />
      </Fragment>
    );
  } else if (feedbackSubmissionStatus === "loading") {
    return <p>Enviando opinión...</p>;
  } else if (feedbackSubmissionStatus === "error") {
    return (
      <p>
        Ocurrió un error mientras enviábamos tu opinión.{" "}
        <button
          onClick={() => setFeedbackSubmissionStatus("idle")}
          class="underline"
        >
          {" "}
          Reintentar{" "}
        </button>
      </p>
    );
  } else {
    return <p>Tu opinión fue regristrada con éxito, ¡muchas gracias!</p>;
  }
}
