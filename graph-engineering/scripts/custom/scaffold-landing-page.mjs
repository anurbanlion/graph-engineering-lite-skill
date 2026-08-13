import { access, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const [targetPagePath, pageSlug] = process.argv.slice(2);

function fail(message) {
  console.error(message);
  process.exitCode = 1;
}

if (!targetPagePath || !pageSlug) {
  fail("Usage: scaffold-landing-page.mjs <target-page-path> <page-slug>");
} else if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(pageSlug)) {
  fail(`Invalid landing-page slug: ${pageSlug}`);
} else {
  const resolvedPagePath = path.resolve(process.cwd(), targetPagePath);

  try {
    await access(resolvedPagePath);
    fail(`Refusing to overwrite existing page: ${targetPagePath}`);
  } catch (error) {
    if (error?.code !== "ENOENT") {
      throw error;
    }

    await mkdir(path.dirname(resolvedPagePath), { recursive: true });
    await writeFile(resolvedPagePath, buildPageSource(pageSlug), "utf8");
    console.log(JSON.stringify({
      status: "created",
      pagePath: targetPagePath,
      pageSlug,
    }));
  }
}

function buildPageSource(slug) {
  return `import { cache } from "react";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getLandingDataV2 } from "@shared/utils/contentful-data/contentful-data.util";
import { pageSeoToMetadata } from "@shared/utils/contentful-metadata/contentful-metadata.util";
import { LeadsProvider } from "@journeys/leads/resources/providers";
import { PageJsonLd } from "@shared/components/molecules";
import { Navbar, PreFooterBanner, Footer } from "@shared/components/organisms";

export const dynamic = "force-static";

const PREVIEW = false;
const PAGE_SLUG = ${JSON.stringify(slug)};

const getProps = cache(async () => {
  const landing = await getLandingDataV2(PREVIEW, PAGE_SLUG, {
    sections: [],
  } as const);

  if (!landing) notFound();
  return landing;
});

export async function generateMetadata(): Promise<Metadata> {
  const { pageSeo } = await getProps();
  return pageSeoToMetadata(pageSeo);
}

export default async function LandingPage() {
  const props = await getProps();

  return (
    <LeadsProvider {...props.leadsFormModalOptions}>
      <PageJsonLd structuredData={props.structuredData} />
      <Navbar
        enableOneLink={props.navBarLinkOptions.enableNavBarOneLink}
        oneLinkChannel={props.navBarLinkOptions.navBarOneLinkChannel}
      />
      {/* Hero and section organisms are intentionally added by a later migration step. */}
      {props.sections.preFooterBannerSection && (
        <PreFooterBanner
          className="io-mt-86 io-mt-xl-160"
          {...PreFooterBanner.propsEngine(props.sections.preFooterSection)}
        />
      )}
      {props.footerSection && (
        <Footer {...Footer.propsEngine(props.footerSection)} />
      )}
    </LeadsProvider>
  );
}
`;
}
