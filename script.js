"use client";

// Load the Inkeep script
const inkeepScript = document.createElement("script");
inkeepScript.type = "module";
inkeepScript.src =
  "https://unpkg.com/@inkeep/widgets-embed@0.2.263/dist/embed.js";

document.body.appendChild(inkeepScript);

// find the Mintlify search container
const buttons = Array.from(document.getElementsByTagName("button"));
const searchButtonContainerEl = buttons.find((button) =>
  button.textContent.includes("Search or ask...")
);

const clonedSearchButtonContainerEl = searchButtonContainerEl.cloneNode(true);

// replace with dummy div, required to remove event listeners on it
searchButtonContainerEl.parentNode.replaceChild(
  clonedSearchButtonContainerEl,
  searchButtonContainerEl
);

// Once the script has loaded, load the Inkeep chat components
inkeepScript.addEventListener("load", function () {
  // Settings for the components
  const sharedConfig = {
    baseSettings: {
      apiKey: "c99c3754a78cf9f7d3d389ef9fa7c3d49cdeb18b95050d10",
      integrationId: "cltexfnd9000iy0ufy9oqo6h6",
      organizationId: "org_VKqv6JAjdI85T7aJ",
      primaryBrandColor: "#0c0c0c",
    },
    aiChatSettings: {
      chatSubjectName: "Nixtla",
      botAvatarSrcUrl:
        "https://storage.googleapis.com/organization-image-assets/nixtla-botAvatarSrcUrl-1709853122420.png",
      botAvatarDarkSrcUrl:
        "https://storage.googleapis.com/organization-image-assets/nixtla-botAvatarDarkSrcUrl-1709853121631.png",
      getHelpCallToActions: [
        {
          name: "Ask on Slack",
          url: "https://join.slack.com/t/nixtlaworkspace/shared_invite/zt-135dssye9-fWTzMpv2WBthq8NK0Yvu6A",
          icon: {
            builtIn: "FaSlack",
          },
        },
        {
          name: "View Repositories",
          url: "https://github.com/Nixtla",
          icon: {
            builtIn: "FaGithub",
          },
        },
      ],
      quickQuestions: [
        "How do I train my own model using mlforecast?",
        "How was TimeGPT trained and what's it best for?",
        "How do I make multivariate scoring for hierarchical forecasting?",
      ],
    },
  };

  // for syncing with dark mode
  const colorModeSettings = {
    observedElement: document.documentElement,
    isDarkModeCallback: (el) => {
      return el.classList.contains("dark");
    },
    colorModeAttribute: "class",
  };

  // add the chat button
  const chatButton = Inkeep().embed({
    componentType: "ChatButton",
    colorModeSync: colorModeSettings,
    properties: sharedConfig,
  });

  // insantiate Inkeep modal
  const searchButtonWithCustomTrigger = Inkeep({
    ...sharedConfig.baseSettings,
  }).embed({
    componentType: "CustomTrigger",
    colorModeSync: colorModeSettings,
    properties: {
      ...sharedConfig,
      isOpen: false,
      onClose: () => {
        searchButtonWithCustomTrigger.render({
          isOpen: false,
        });
      },
    },
  });

  // When the Mintlify search bar clone is clicked, open the Inkeep search modal
  clonedSearchButtonContainerEl.addEventListener("click", function () {
    searchButtonWithCustomTrigger.render({
      isOpen: true,
    });
  });
});
