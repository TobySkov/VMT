const css = `
/* notebook specific tweaks so no black outline and matching padding
/* can't be wrapped inside bk-root. here are the offending jupyter lines:
/* https://github.com/jupyter/notebook/blob/master/notebook/static/notebook/less/renderedhtml.less#L59-L76 */
.rendered_html .bk-root .bk-tooltip table,
.rendered_html .bk-root .bk-tooltip tr,
.rendered_html .bk-root .bk-tooltip th,
.rendered_html .bk-root .bk-tooltip td {
  border: none;
  padding: 1px;
}
`;
export default css;
