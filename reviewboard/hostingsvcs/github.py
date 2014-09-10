from reviewboard.admin.server import get_server_url
                                                get_review_request_id)
    def api_get(self, url, *args, **kwargs):
            return data
                      'This code will be sent to you by GitHub.'))
                raise AuthorizationError(rsp['message'])
            raise HostingServiceError(rsp['message'])
            raise HostingServiceError(six.text_type(e))
class GitHub(HostingService):
            'reviewboard.hostingsvcs.github.post_receive_hook_close_submitted',
            name='github-hooks-close-submitted')
    RAW_MIMETYPE = 'application/vnd.github.v3.raw'

    REFNAME_PREFIX = 'refs/heads/'
    REFNAME_PREFIX_LEN = len(REFNAME_PREFIX)

            repo_info = self._api_get_repository(
                self._get_repository_owner_raw(plan, kwargs),
                self._get_repository_name_raw(plan, kwargs))
        except Exception as e:
            if six.text_type(e) == 'Not Found':
                    # If we get a Not Found, then the authorization was
                    if six.text_type(e) != 'Not Found':
        url = self._build_api_url(self._get_repo_api_url(repository),
                                  'git/blobs/%s' % revision)

        try:
            return self.client.http_get(url, headers={
                'Accept': self.RAW_MIMETYPE,
            })[0]
        except (URLError, HTTPError):
            raise FileNotFoundError(path, revision)
        url = self._build_api_url(self._get_repo_api_url(repository),
                                  'git/blobs/%s' % revision)

            self.client.http_get(url, headers={
                'Accept': self.RAW_MIMETYPE,
            })

        except (URLError, HTTPError):

        url = self._build_api_url(self._get_repo_api_url(repository),
                                  'git/refs/heads')

        try:
            rsp = self.client.api_get(url)
        except Exception as e:
            logging.warning('Failed to fetch commits from %s: %s',
                            url, e)
            return results

        for ref in rsp:
            refname = ref['ref']

            if refname.startswith(self.REFNAME_PREFIX):
                name = refname[self.REFNAME_PREFIX_LEN:]
                results.append(Branch(id=name,
                                      commit=ref['object']['sha'],
                                      default=(name == 'master')))

        resource = 'commits'
        url = self._build_api_url(self._get_repo_api_url(repository), resource)

        if start:
            url += '&sha=%s' % start

        try:
            rsp = self.client.api_get(url)
        except Exception as e:
            logging.warning('Failed to fetch commits from %s: %s',
                            url, e)
            return results

        for item in rsp:
            url = self._build_api_url(repo_api_url, 'commits')
            url += '&sha=%s' % revision

            try:
                commit = self.client.api_get(url)[0]
            except Exception as e:
                raise SCMError(six.text_type(e))
        # Step 2: fetch the "compare two commits" API to get the diff if the
        # commit has a parent commit. Otherwise, fetch the commit itself.
        if parent_revision:
            url = self._build_api_url(
                repo_api_url, 'compare/%s...%s' % (parent_revision, revision))
        else:
            url = self._build_api_url(repo_api_url, 'commits/%s' % revision)

        try:
            comparison = self.client.api_get(url)
        except Exception as e:
            raise SCMError(six.text_type(e))

        if parent_revision:
            tree_sha = comparison['base_commit']['commit']['tree']['sha']
        else:
            tree_sha = comparison['commit']['tree']['sha']

        files = comparison['files']
        url = self._build_api_url(repo_api_url, 'git/trees/%s' % tree_sha)
        url += '&recursive=1'
        tree = self.client.api_get(url)
        return '%s?access_token=%s' % (
            '/'.join(api_paths),
            self.account.data['authorization']['token'])
    def _api_get_repository(self, owner, repo_name):
        return self.client.api_get(self._build_api_url(
            self._get_repo_api_url_raw(owner, repo_name)))

def post_receive_hook_close_submitted(request, local_site_name=None,
                                      repository_id=None,
                                      hosting_service_id=None):
        return HttpResponse(status=400)
    server_url = get_server_url(request=request)
    review_request_id_to_commits = \
        _get_review_request_id_to_commits_map(payload, server_url)
    if review_request_id_to_commits:
        close_all_review_requests(review_request_id_to_commits,
                                  local_site_name, repository_id,
                                  hosting_service_id)
def _get_review_request_id_to_commits_map(payload, server_url):
    review_request_id_to_commits_map = defaultdict(list)
        review_request_id_to_commits_map[review_request_id].append(
            '%s (%s)' % (branch_name, commit_hash[:7]))
    return review_request_id_to_commits_map