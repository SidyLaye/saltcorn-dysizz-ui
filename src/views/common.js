/* configuration commune des vues maison : un formulaire d'une étape */
"use strict";
const configWorkflow = (fields, help) => () => {
  const Workflow = require("@saltcorn/data/models/workflow");
  const Form = require("@saltcorn/data/models/form");
  return new Workflow({
    steps: [{
      name: "Réglages",
      form: async () => new Form({ blurb: help || "", fields: typeof fields === "function" ? await fields() : fields }),
    }],
  });
};
const code = (name, label, sublabel) => ({ name, label, sublabel, type: "String", fieldview: "textarea", attributes: { rows: 14, spellcheck: false } });
const str = (name, label, sublabel, extra = {}) => ({ name, label, sublabel, type: "String", ...extra });
const int = (name, label, sublabel, def) => ({ name, label, sublabel, type: "Integer", default: def });
const tableOptions = async () => {
  const Table = require("@saltcorn/data/models/table");
  return (await Table.find({})).map((t) => t.name).filter((n) => n !== "users").join(",");
};
const viewOptions = async () => {
  const View = require("@saltcorn/data/models/view");
  return ["", ...(await View.find({})).map((v) => v.name)].join(",");
};
module.exports = { configWorkflow, code, str, int, tableOptions, viewOptions };
