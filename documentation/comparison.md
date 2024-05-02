| Feature | treqs | doorstop | word processor | spreadsheet | traditional re tools | issue tracker[^issue-1] | Eclipse Capra |
| ---     | ---   | ---      | ---            | ---         | ---                  | ---                     | ---     |
| **Traceability** |
| Supports unique IDs | yes (UID) | yes (user defined pattern, use filename and git to avoid ID collisions) | no | no | yes | yes[^jira-1] | no |
| Supports traceability | yes | yes | no | to some extend, through handwritten ids  | yes | yes[^jira-2] | yes |
| Allows complex tracelinks, e.g. additional attributes and types | yes | no | no | no | yes | partially[^jira-3] | yes | 
| Allow tracelink from test to requirement in existing testfiles | yes | no | no | no | likely, but impossible to keep in sync with git | partially[^jira-4] | yes[^capra-1] |
| Allow several traceable elements in a single file, so that reading flow is supported | yes | no | yes | yes | yes, but license required | indirectly[^jira-5] | yes |
| **Version control** |
| Supports baselining | yes, through git | yes, through git | to some extent, through sharepoint and change control | no | yes | no | no |
| Integrates with code and tests on git | yes | partially[^doorstop-1] | no | no | no | yes[^jira-6] | no |
| **Interoperability and recoverability** | 
| Needs/supports additional scripting and infrastructure to integrate in processes | yes | yes | no | partially | yes | no scripting, but configuration needed | no |
| Scripting interface | forthcoming, python | yes, python | no | partially | yes, proprietory | indirectly[^jira-7] | no |
| Requirements stored in an accessible format | yes | yes [^doorstop-1] | yes | yes | no | no | N/A[^capra-2] |
| Requirements stored in a human readable format | yes | no [^doorstop-1] | yes | yes | no | no |
| Open source | yes, MIT | yes, LGPL | no | no | no | no | N/A[^capra-2] |
| **Collaboration at scale** |
| Can easily provide rw access to a large number of developers | yes | yes | no | no | no | yes | no |
| Generate views and reports | forthcoming | yes, html | no | no | yes | yes | yes |
| Allows peer-reviewing of requirements between Developers | yes | yes [^doorstop-2]) | no | no | no | yes | no |
| **Advanced features** | 
| Consistency checks | yes | yes | no | no | yes | unclear | yes[^capra-3] |
| Allows adjusting of requirements/traceability information model | yes, per project | no | no | no | yes, per instance | yes, per project | yes[^capra-4] |
| Allows graphical modeling | yes, plantuml | unsure | yes | partially | yes | no[^jira-8] | yes[^capra-5] |
| Allows to review changes and merging of graphical modeling | yes, plantuml diff in git merge | unsure | no | no | no | no | no |
| Support for regulation and standards | commercial options forthcoming (considering ISO26262, SOTIF, HiPAA, ISO 27001) | unsure | no | no | usually yes | no | yes[^capra-6] |

[^doorstop-1]: Requirements are managed in yaml configuration files, that do not emphasize human readability in the same way as treqs' markdown files. To see requirements in their context, one needs to generate the html document

[^doorstop-2]: Doorstop has a more formal view on reviews of requirements and tracelinks, taking note of which item has been reviewed and confirmed. It has a strict, yet static state model about requirements as well. In contrast, treqs treats requirements similar to code in git - where you would also not review and confirm individual lines (unless you are in a cleanroom scenario). These are different philosophies, treqs perhaps pushing more for an agile mindset and doorstop more for a strict, plan-driven mindset.

[^issue-1]: Considered plain JIRA for assessing the features. There is an extension for JIRA that would support some more requirements-related features (https://marketplace.atlassian.com/apps/1213064/r4j-requirements-management-for-jira?hosting=server&tab=overview). It is charged separately, since it is offered by a third party. It contains predefined relationship types, overviews for requirements and mechanisms for organizing them, baselines, imports and exports.

[^jira-1]: JIRA generates a unique identifier for each issue in the format "\<project-id>-\<number>".

[^jira-2]: JIRA allows linking of issues.

[^jira-3]: JIRA supports different types of relationships (additional custom types can be configured). JIRA does not support attributes of relationships.

[^jira-4]: If tests (such as user tests with the plugin Zephyr) are managed in JIRA, linking to requirements is convenient by linking the issues. Linking between issues and git-commits (and thus contents of a repository, i.e., tests) is possible after linking the repository with JIRA. However, then during the commit, the issue identifier has to be provided so that the commit (not the affected files themselves) is linked to the issue containing the requirement. This means, from a requirement it is possible to get to the related commits in git. The reverse direction needs to be maintained manually.

[^jira-5]: If JIRA and Confluence are used together and linked, it is possible to create pages that use contents of JIRA tickets (by reference). These pages can combine hard-coded content on the page itself with content and meta-data of issues. In JIRA itself, views can be created via filters, but those results are less readable than on a dedicated page.

[^jira-6]: Based on commit messages that contain the issues' identifiers.

[^jira-7]: Support via third-party extensions.

[^jira-8]: There is a Draw.io integration to Confluence for modeling support.

[^capra-1]: Eclipse Capra 0.8.2 supports embedded trace link annotations for Java and C.

[^capra-2]: Eclipse Capra does not manage requirements. They can be stored in an arbitrary format that is supported by Eclipse Capra, however, including ReqIF, Word, or Excel.

[^capra-3]: Eclipse Capra enforces consistency by only allowing the creation of traceability links that are correct according to the TIM.

[^capra-4]: Eclipse Capra's TIM is stored as an ecore model and can be changed to accommodate specific needs.

[^capra-5]: Eclipse Capra visualises the trace links using PlantUML, a sunburst viewer, or as a traceability matrix. However, these views cannot be manipulated and it thus does not support "modelling" in the strict sense of the word.

[^capra-6]: Eclipse Capra supports the traceability link types required by specific regulations via its customisable TIM and supports producing reports that are necessary to show compliance via its reporting and visualisation features.