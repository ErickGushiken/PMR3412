import App from "./App.svelte";

const app = new App({
  target: document.body,
  props: {
    name: "WebSockets Echo",
  },
});

export default app;
