const siteDir = process.env.SITE_DIR || "_site";

module.exports = {
  content: [`${siteDir}/**/*.html`, `${siteDir}/**/*.js`],
  css: [`${siteDir}/assets/css/*.css`],
  output: `${siteDir}/assets/css/`,
  skippedContentGlobs: [`${siteDir}/assets/**/*.html`],
};
