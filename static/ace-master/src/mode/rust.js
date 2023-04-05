/*
  THIS FILE WAS AUTOGENERATED BY mode.tmpl.js
*/

"use strict";

var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var RustHighlightRules = require("./rust_highlight_rules").RustHighlightRules;
var FoldMode = require("./folding/cstyle").FoldMode;

var Mode = function() {
    this.HighlightRules = RustHighlightRules;
    this.foldingRules = new FoldMode();
    this.$behaviour = this.$defaultBehaviour;
};
oop.inherits(Mode, TextMode);

(function() {
    this.lineCommentStart = "//";
    this.blockComment = {start: "/*", end: "*/", nestable: true};
    this.$quotes = { '"': '"' };
    this.$id = "ace/mode/rust";
}).call(Mode.prototype);

exports.Mode = Mode;
