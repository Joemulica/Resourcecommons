// Resource Commons settings. Paste links from Stripe and Kit here.
// Anything left blank shows as "opening soon" on the site.
window.RC = {
  // Kit (newsletter): the number in your Kit form's URL, e.g. app.kit.com/forms/1234567
  kitFormId: "",

  // Exhibitor application or invoice request form (Tally or Google Forms)
  exhibit: "",

  // Stripe Payment Links, one per table option. Name each Stripe product with its code first,
  // e.g. "SOF27 Standard table", so the reconciliation workbook can sort it by fair.
  pay: {
    "SOF27-1": "", "SOF27-2": "", "SOF27-3": "",
    "SNR27-1": "",
    "FAF27-1": "",
    "FSP27-1": "", "FSP27-2": "", "FSP27-3": "",
    "CAP27-1": ""
  },

  // Stripe Payment Links for guides. In each link's settings, choose
  // "Don't show confirmation page - redirect to your website" and use
  // https://resourcecommons.com/guide-thanks.html?g=CODE  (CODE = SOF27, ..., or BUNDLE)
  guide: { SOF27: "", SNR27: "", FAF27: "", FSP27: "", CAP27: "", BUNDLE: "" },

  // Where each guide PDF lives (e.g. a Google Drive share link). Shown only on the thank-you page.
  download: { SOF27: "", SNR27: "", FAF27: "", FSP27: "", CAP27: "" }
};
