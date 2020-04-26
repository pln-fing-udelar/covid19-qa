import { useState, useEffect, useCallback } from "preact/hooks";

// Hook taken from: https://usehooks.com/
const useAsync = (asyncFunction, immediate = true) => {
  const [state, setState] = useState({
    status: "idle",
    data: null,
    error: null,
  });

  // The execute function wraps asyncFunction and

  // handles setting state for pending, value, and error.

  // useCallback ensures the below useEffect is not called

  // on every render, but only if asyncFunction changes.

  const execute = useCallback(() => {
    setState({ status: "loading", data: null, error: null });

    return asyncFunction()
      .then((result) =>
        setState({ status: "success", data: result, error: null })
      )
      .catch((error) => {
        if (process.env.NODE_ENV === "development") {
          console.error(
            `${error}
The above error ocurred while calling the async function: 
${asyncFunction}.`
          );
        }
        setState({ status: "error", data: null, error });
      });
  }, [asyncFunction]);

  // Call execute if we want to fire it right away.

  // Otherwise execute can be called later, such as

  // in an onClick handler.

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { execute, ...state };
};

export default useAsync;
