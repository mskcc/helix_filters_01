"use strict";function _typeof(e){return(_typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function e(t){return typeof t}:function e(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(e)}function _classCallCheck(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function _defineProperties(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function _createClass(e,t,r){return t&&_defineProperties(e.prototype,t),r&&_defineProperties(e,r),e}
/**
 * @license 
 * Copyright (c) 2018, Immo Schulz-Gerlach, www.isg-software.de 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are 
 * permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of
 * conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list
 * of conditions and the following disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
 * SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
 * TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
 * WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
/**
 * @license 
 * Copyright (c) 2018, Immo Schulz-Gerlach, www.isg-software.de 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are 
 * permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of
 * conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list
 * of conditions and the following disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
 * SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
 * TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
 * WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
!function(p){function i(e,t){var r=p.extend({},t,e);if("string"==typeof r.preset){var n=p.fn.prependFoldingArrowIcon.PRESETS[r.preset];"object"===_typeof(n)&&p.extend(r,n,e)}else r.preset instanceof l&&p.extend(r,r.preset.preset,e);return r}function r(e){for(var t=e.split(" "),r="",n=0,o=t.length;n<o;n++)r+="."+t[n];return r}function n(e){var t=document.createElementNS(d,"svg"),r=-e.viewboxRadius-e.viewboxMargin,n=2*(e.viewboxRadius+e.viewboxMargin);return t.setAttribute("viewBox",r+" "+r+" "+n+" "+n),t.setAttribute("width",n),t.setAttribute("height",n),t.setAttribute("class",e.svgClass),t}function o(e,t){var r=document.createElementNS(d,"g");e.appendChild(r);for(var n=0,o=t.graph.length;n<o;n++){var i=t.graph[n],a=document.createElementNS(d,i.element);for(var s in i.attributes)a.setAttribute(s,i.attributes[s]+(t.closePath&&"path"===i.element?"z":""));r.appendChild(a)}}function a(){var e=this.firstChild;if(e&&3===e.nodeType){var t=e.textContent,r=t.replace(/^\s+/g,"");r!==t&&(e.textContent=r)}}function s(){var e=this.lastChild;if(e&&3===e.nodeType){var t=e.textContent,r=t.replace(/\s+$/g,"");r!==t&&(e.textContent=r)}}function c(e,t){return p("svg"+r(t.svgClass),e).first()}function f(e,t,r){if(t.titleShowing||t.titleHidden){var n=r;void 0===n&&(n=c(e,t));var o=p("> title",n),i=e.is(t.ifIsSelector)?t.titleShowing:t.titleHidden;if("string"==typeof i){if(!o.length){var a=document.createElementNS(d,"title");n.prepend(a),o=p(a)}o.text(i)}else o.text("")}}function e(e){return new l(e)}var l=function(){function t(e){_classCallCheck(this,t),this.preset=p.extend({},p.fn.prependFoldingArrowIcon.PRESETS[e]),Array.isArray(this.preset.graph)&&(this.preset.graph=this.preset.graph.slice())}return _createClass(t,[{key:"prependToGraph",value:function e(t,r){return this.preset.graph.unshift({element:t,attributes:r}),this}},{key:"appendToGraph",value:function e(t,r){return this.preset.graph.push({element:t,attributes:r}),this}},{key:"prop",value:function e(t,r){return void 0===r?this.preset[t]:(this.preset[t]=r,this)}}]),t}(),d="http://www.w3.org/2000/svg";p.fn.prependFoldingArrowIcon=function(e){var t=i(e,p.fn.prependFoldingArrowIcon.DEFAULTS),r=n(t);return o(r,t),this.each(a).prepend(r,t.separator).addClass(t.containerClass),this},p.fn.appendFoldingArrowIcon=function(e){var t=i(e,p.fn.prependFoldingArrowIcon.DEFAULTS),r=n(t);return o(r,t),this.each(s).append(t.separator,r).addClass(t.containerClass),this};var u="foldingArrowIconTransformationSetup";p.fn.setupFoldingArrowIconTransformation=function(n){var o=i(n,p.fn.transformFoldingArrowIcon.DEFAULTS);return this.each(function(){var e=p(this).data(u),t="object"===_typeof(e)?p.extend({},e,n):o,r;f(p(this).data(u,t),o)}),this},p.fn.transformFoldingArrowIcon=function(){var l=p.fn.transformFoldingArrowIcon.DEFAULTS;return this.each(function(){var e=p(this),t=e.data(u);"object"!==_typeof(t)&&(t=l);var r=c(e,t);f(e,t,r);for(var n=0,o=t.transformations.length;n<o;n++){var i=t.transformations[n];for(var a in i){var s=p(a,r);e.is(t.ifIsSelector)?s.attr("transform",i[a]):s.removeAttr("transform")}}}),this},p.fn.appendFoldingArrowIcon.PRESETS=p.fn.prependFoldingArrowIcon.PRESETS={"arrow-right":{graph:[{element:"path",attributes:{d:"M-3,-5 L5,0 L-3,5"}}],closePath:!0},"arrow-up-down":{graph:[{element:"path",attributes:{d:"M-5,-3 L0,5 L5,-3"}}],closePath:!0,svgClass:"folding-arrow-icon updown",transformations:[{">g":"scale(1 -1)"}]},plus:{graph:[{element:"line",attributes:{x1:"-10",y1:"0",x2:"10",y2:"0",class:"h"}},{element:"line",attributes:{x1:"0",y1:"-10",x2:"0",y2:"10",class:"v"}}],svgClass:"folding-arrow-icon plus",viewboxRadius:10,viewboxMargin:1,transformations:[{">g":"rotate(45)"}]},burger:{containerClass:"burger",svgClass:"burger-icon",viewboxRadius:15,viewboxMargin:3,graph:[{element:"line",attributes:{x1:"-15",y1:"-10",x2:"15",y2:"-10",class:"topline"}},{element:"line",attributes:{x1:"-15",y1:"0",x2:"15",y2:"0",class:"midline"}},{element:"line",attributes:{x1:"-15",y1:"10",x2:"15",y2:"10",class:"bottomline"}}],transformations:[{"line.topline":"translate(0,10)"},{"line.bottomline":"translate(0,-10)"},{"line.midline":"rotate(90)"},{g:"rotate(45)"}]},dash:{graph:[{element:"line",attributes:{x1:"-3",x2:"5",y1:"0",y2:"0"}}],svgClass:"folding-arrow-icon static dash"},disc:{graph:[{element:"circle",attributes:{cx:"0",cy:"0",r:"3"}}],svgClass:"folding-arrow-icon static disc"}},p.fn.prependFoldingArrowIcon.PRESETS["plus-minus"]=e("plus").prop("svgClass","folding-arrow-icon plus-minus").prop("transformations",[{"line.v":"scale(1 0)"}]).preset,p.fn.appendFoldingArrowIcon.copyOfPreset=p.fn.prependFoldingArrowIcon.copyOfPreset=e,p.fn.appendFoldingArrowIcon.DEFAULTS=p.fn.prependFoldingArrowIcon.DEFAULTS=p.extend({},{svgClass:"folding-arrow-icon",containerClass:"folding-arrow",separator:"&ensp;",viewboxRadius:5,viewboxMargin:1,graph:void 0,closePath:!0,preset:void 0},p.fn.prependFoldingArrowIcon.PRESETS["arrow-right"]),p.fn.transformFoldingArrowIcon.DEFAULTS=p.extend({ifIsSelector:".showing",transformations:[{"> g":"rotate(90)"}],titleShowing:void 0,titleHidden:void 0},p.fn.prependFoldingArrowIcon.DEFAULTS)}(jQuery);