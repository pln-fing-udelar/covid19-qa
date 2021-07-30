import { Fragment } from "preact";
import { useState } from "preact/hooks";
import {
  ExactMatchFeedbackButton,
  ContainedMatchFeedbackButton,
  IncompleteMatchFeedbackButton,
  NoMatchFeedbackButton,
  UnrelatedParagraphFeedbackButton,
  RelatedParagraphFeedbackButton,
  GoodParagraphFeedbackButton,
} from "./feedbackButtons";
import { answerFeedbackChoices, paragraphFeedbackChoices }  from "./feedbackChoices";
import { postParagraphFeedback, postAnswerFeedback } from "../../utils/api-client";

function answerFeedbackSection(answerId, answerFeedbackSubmissionStatus, setAnswerFeedbackSubmissionStatus, onAnswerFeedbackSubmit) {
  if (answerFeedbackSubmissionStatus === "idle") {
    return (
      <section class="mt-7" style="height: 125px">
        <span>Calificar el segmento resaltado:</span>
        <div class="mt-2 pl-5">
          <NoMatchFeedbackButton
            onClick={() => onAnswerFeedbackSubmit(answerId, answerFeedbackChoices.noMatch)}
          />
        </div>
        <div class="pl-5">
          <IncompleteMatchFeedbackButton
            onClick={() => onAnswerFeedbackSubmit(answerId, answerFeedbackChoices.incompleteMatch)}
          />
        </div>
        <div class="pl-5">
          <ContainedMatchFeedbackButton
            onClick={() => onAnswerFeedbackSubmit(answerId, answerFeedbackChoices.containedMatch)}
          />
        </div>
        <div class="pl-5">
          <ExactMatchFeedbackButton
            onClick={() => onAnswerFeedbackSubmit(answerId, answerFeedbackChoices.exactMatch)}
          />
        </div>
      </section>
    )
  } else if (answerFeedbackSubmissionStatus === "loading") {
    return <p>Enviando opinión...</p>;
  } else if (answerFeedbackSubmissionStatus === "error") {
    return (
      <p>
        Ocurrió un error mientras enviábamos tu opinión.{" "}
        <button
          onClick={() => setAnswerFeedbackSubmissionStatus("idle")}
          class="underline"
        >
          {" "}
          Reintentar{" "}
        </button>
      </p>
    );
  } else {
    return <p>Tu opinión fue registrada con éxito, ¡muchas gracias!</p>;
  }
}

function paragraphFeedbackSection(answerId, paragraphFeedbackSubmissionStatus, setParagraphFeedbackSubmissionStatus, onParagraphFeedbackSubmit) {
  if (paragraphFeedbackSubmissionStatus === "idle") {
    return (
      <section style="height: 125px">
        <span>Calificar el párrafo:</span>
        <div class="mt-2 pl-5">
          <UnrelatedParagraphFeedbackButton
            onClick={() => onParagraphFeedbackSubmit(answerId, paragraphFeedbackChoices.unrelated)}
        />
        </div>
        <div class="pl-5">
          <RelatedParagraphFeedbackButton
            onClick={() => onParagraphFeedbackSubmit(answerId, paragraphFeedbackChoices.related)}
          />
        </div>
        <div class="pl-5">
          <GoodParagraphFeedbackButton
            onClick={() => onParagraphFeedbackSubmit(answerId, paragraphFeedbackChoices.containsAnswer)}
          />
        </div>
      </section>
    )
  } else if (paragraphFeedbackSubmissionStatus === "loading") {
    return <p>Enviando opinión...</p>;
  } else if (paragraphFeedbackSubmissionStatus === "error") {
    return (
      <p>
        Ocurrió un error mientras enviábamos tu opinión.{" "}
        <button
          onClick={() => setParagraphFeedbackSubmissionStatus("idle")}
          class="underline"
        >
          {" "}
          Reintentar{" "}
        </button>
      </p>
    );
  } else {
    return <p>Tu opinión fue registrada con éxito, ¡muchas gracias!</p>;
  }
}

export default function FeedbackSection({ answerId }) {
  const [answerFeedbackSubmissionStatus, setAnswerFeedbackSubmissionStatus] = useState(
    "idle"
  );
  const [paragraphFeedbackSubmissionStatus, setParagraphFeedbackSubmissionStatus] = useState(
    "idle"
  );

  const onParagraphFeedbackSubmit = (answerId, feedbackChoice) => {
    setParagraphFeedbackSubmissionStatus("loading");
    postParagraphFeedback(answerId, feedbackChoice)
      .then(() => setParagraphFeedbackSubmissionStatus("success"))
      .catch(() => {
        setParagraphFeedbackSubmissionStatus("error");
      });
  };

  const onAnswerFeedbackSubmit = (answerId, feedbackChoice) => {
    setAnswerFeedbackSubmissionStatus("loading");
    postAnswerFeedback(answerId, feedbackChoice)
      .then(() => setAnswerFeedbackSubmissionStatus("success"))
      .catch(() => {
        setAnswerFeedbackSubmissionStatus("error");
      });
  };

  return (
    <Fragment>
      <div class="container w-50">
        {paragraphFeedbackSection(answerId, paragraphFeedbackSubmissionStatus, setParagraphFeedbackSubmissionStatus, onParagraphFeedbackSubmit)}
      </div>
      <div class="container w-50 mb-3">
        {answerFeedbackSection(answerId, answerFeedbackSubmissionStatus, setAnswerFeedbackSubmissionStatus, onAnswerFeedbackSubmit)}
      </div>
    </Fragment>
  );
}
