// ==UserScript==
// @name         Cubari Custom Reader
// @namespace    http://tampermonkey.net/ 
// @version      0.4
// @description  Custom manga reader using Cubari UI
// @author       You
// @match        *://*/*
// @grant        GM_registerMenuCommand
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function() {
    'use strict';

    // Placeholders replaced by build script
    const combined_css = CSS_PLACEHOLDER;
    const combined_js = JS_PLACEHOLDER;
    const reader_html = HTML_PLACEHOLDER;

    let activeIframe = null;

    function startReader(imagesJSON) {
        if (activeIframe) return;

        const iframe = document.createElement('iframe');
        activeIframe = iframe;
        iframe.style.position = 'fixed';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.width = '100vw';
        iframe.style.height = '100vh';
        iframe.style.border = 'none';
        iframe.style.zIndex = '999999';
        document.body.appendChild(iframe);

        // Load saved settings for the reader
        const savedSettings = GM_getValue('reader_settings', {});

        // Construct script content
        // We use a self-invoking function inside the iframe to avoid polluting global scope more than necessary
        const scriptContent = `
            window.BASE_API_PATH = "";
            window.IS_FIRST_PARTY = false;
            window.IS_INDEXED = false;
            window.IMAGE_PROXY_URL = "";
            window.version_query = "";
            window.tag = window.tag || (() => {});

            // Shim localStorage to persist settings across domains
            (function() {
                try {
                    const store = ${JSON.stringify(savedSettings)};
                    const myLocalStorage = {
                        getItem: function(key) { return store[key] || null; },
                        setItem: function(key, value) {
                            store[key] = String(value);
                            window.parent.postMessage({ type: 'cubari-save-setting', key: key, value: String(value) }, '*');
                        },
                        removeItem: function(key) {
                            delete store[key];
                            window.parent.postMessage({ type: 'cubari-delete-setting', key: key }, '*');
                        },
                        clear: function() {
                            for (var member in store) delete store[member];
                        },
                        key: function(i) { return Object.keys(store)[i] || null; },
                        get length() { return Object.keys(store).length; }
                    };
                    
                    Object.defineProperty(window, 'localStorage', {
                        value: myLocalStorage,
                        writable: true,
                        configurable: true
                    });
                } catch(e) {
                    console.error("Cubari Reader: Failed to shim localStorage", e);
                }
            })();

            ${combined_js}

            (function() {
                const extractedImages = ${imagesJSON};
                if (window.Reader) {
                    const data = {
                        title: "Extracted Series",
                        slug: "custom",
                        chapters: {
                            "1": {
                                title: "Extracted Images",
                                chapter: "1",
                                volume: "1",
                                groups: { "Extracted": extractedImages },
                                loaded: { "Extracted": true },
                                images: { "Extracted": extractedImages },
                                wides: { "Extracted": [] },
                                descriptions: { "Extracted": [] },
                                previews: { "Extracted": [] }
                            }
                        },
                        chaptersIndex: ["1"],
                        volMap: {"1": "1"},
                        groups: {"Extracted": "Extracted"},
                        preferred_sort: ["Extracted"]
                    };

                    const SCP = {
                        series: "custom",
                        chapter: "1",
                        page: 0,
                        group: "Extracted"
                    };

                    window.API.requestSeries = () => Promise.resolve(data);
                    Reader.updateData(data);
                    Reader.displaySCP(SCP);

                    const logo = document.querySelector(".ico-btn.guya");
                    if (logo) {
                        logo.onclick = (e) => {
                            e.preventDefault();
                            window.parent.postMessage("close-cubari-reader", "*");
                        };
                        logo.style.cursor = "pointer";
                        if (window.Tooltippy) Tooltippy.attach(logo, "Exit Reader [Esc]");
                    }
                }

                document.addEventListener("keydown", (e) => {
                    if (e.key === "Escape") {
                        if (window.Loda && window.Loda.open) return;
                        window.parent.postMessage("close-cubari-reader", "*");
                    }
                }, true);
            })();
        `;

        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.open();
        doc.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><style>' + combined_css + '</style></head><body>' + reader_html + '</body></html>');
        doc.close();

        const script = doc.createElement('script');
        script.textContent = scriptContent;
        doc.body.appendChild(script);
        iframe.focus();
    }

    window.addEventListener('message', (event) => {
        if (event.data === 'close-cubari-reader') {
            if (activeIframe) {
                document.body.removeChild(activeIframe);
                activeIframe = null;
            }
        }
        if (event.data && event.data.type === 'cubari-save-setting') {
            const settings = GM_getValue('reader_settings', {});
            settings[event.data.key] = event.data.value;
            GM_setValue('reader_settings', settings);
        }
        if (event.data && event.data.type === 'cubari-delete-setting') {
            const settings = GM_getValue('reader_settings', {});
            delete settings[event.data.key];
            GM_setValue('reader_settings', settings);
        }
    });

    function extractImages(selector) {
        const elements = document.querySelectorAll(selector);
        const images = [];
        elements.forEach(el => {
            if (el.tagName === 'IMG') {
                if (el.src && el.src.startsWith('http')) images.push(el.src);
            } else if (el.tagName === 'CANVAS') {
                try { images.push(el.toDataURL()); } catch(e) {}
            } else {
                const bg = window.getComputedStyle(el).backgroundImage;
                if (bg && bg !== 'none') {
                    const match = bg.match(/url\((['"]?)(.*?)\1\)/);
                    if (match && match[2]) images.push(match[2]);
                }
            }
        });
        return images;
    }

    GM_registerMenuCommand("Launch Cubari Reader", () => {
        const hostname = window.location.hostname;
        const savedSelector = GM_getValue('selector_' + hostname, 'img');
        const selector = prompt('Enter CSS selector for images (e.g. img, .manga-page):', savedSelector);
        if (selector) {
            if (selector !== savedSelector) {
                GM_setValue('selector_' + hostname, selector);
            }
            const images = extractImages(selector);
            if (images.length > 0) {
                startReader(JSON.stringify(images));
            } else {
                alert('No images found with that selector!');
            }
        }
    });

})();