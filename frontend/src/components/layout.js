function Layout({ children }) {
  return (
    <main class="px-4 sm:px-8 md:px-16 lg:px-32 max-w-6xl w-full sm:w-9/12 bg-gray-300 shadow rounded-md py-8 m-4 md:m-8">
      {children}
    </main>
  );
}

export default Layout;
