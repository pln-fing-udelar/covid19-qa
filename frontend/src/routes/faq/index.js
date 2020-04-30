import FaqHeader from "../../components/faqHeader";
import FormattedAnswer from "../../components/formattedAnswer";
import FaqMetadata from "../../components/faqMetadata";
import Layout from "../../components/layout";
import useAsync from "../../hooks/useAsync";
import { getFAQ } from "../../utils/api-client";
import FaqLoader from "./faqLoader";

export default function Faq() {
  const { data: faqData, status } = useAsync(getFAQ);
  return (
    <Layout>
      <section class="text-gray-800">
        <div class="mb-8">
          <FaqHeader />
        </div>
        {status === "idle" || status === "loading" ? (
          <FaqLoader />
        ) : status === "error" ? (
          <p>
            Ocurrió un error mientras cargábamos las preguntas frecuentes.
            Inténtalo de nuevo más tarde.
          </p>
        ) : (
          faqData.map((q) => (
            <div class="mb-8">
              <h3 class="font-semibold text-lg mb-2">{q.title}</h3>
              <p>
                <FormattedAnswer
                  answerStartIndex={q.answer_start_index}
                  asnwerEndIndex={q.answer_end_index}
                >
                  {q.context}
                </FormattedAnswer>
              </p>
              <hr class="my-1" />
              <FaqMetadata faq={q} />
            </div>
          ))
        )}
      </section>
    </Layout>
  );
}
