import hashlib
import hmac
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.six.moves.urllib.parse import urljoin
from reviewboard.admin.server import build_server_url, get_server_url
                                                get_repository_for_hook,
    has_repository_hook_instructions = True

    def get_repository_hook_instructions(self, request, repository):
        """Returns instructions for setting up incoming webhooks."""
        plan = repository.extra_data['repository_plan']
        add_webhook_url = urljoin(
            self.account.hosting_url or 'https://github.com/',
            '%s/%s/settings/hooks/new'
            % (self._get_repository_owner_raw(plan, repository.extra_data),
               self._get_repository_name_raw(plan, repository.extra_data)))

        webhook_endpoint_url = build_server_url(local_site_reverse(
            'github-hooks-close-submitted',
            local_site=repository.local_site,
            kwargs={
                'repository_id': repository.pk,
                'hosting_service_id': repository.hosting_account.service_name,
            }))

        example_id = 123
        example_url = build_server_url(local_site_reverse(
            'review-request-detail',
            local_site=repository.local_site,
            kwargs={
                'review_request_id': example_id,
            }))

        return render_to_string(
            'hostingsvcs/github/repo_hook_instructions.html',
            RequestContext(request, {
                'example_id': example_id,
                'example_url': example_url,
                'repository': repository,
                'server_url': get_server_url(),
                'add_webhook_url': add_webhook_url,
                'webhook_endpoint_url': webhook_endpoint_url,
                'hook_uuid': repository.get_or_create_hooks_uuid(),
            }))

    hook_event = request.META.get('HTTP_X_GITHUB_EVENT')

    if hook_event == 'ping':
        # GitHub is checking that this hook is valid, so accept the request
        # and return.
        return HttpResponse()
    elif hook_event != 'push':
        return HttpResponseBadRequest(
            'Only "ping" and "push" events are supported.')

    repository = get_repository_for_hook(repository_id, hosting_service_id,
                                         local_site_name)

    # Validate the hook against the stored UUID.
    m = hmac.new(bytes(repository.get_or_create_hooks_uuid()), request.body,
                 hashlib.sha1)

    sig_parts = request.META.get('HTTP_X_HUB_SIGNATURE').split('=')

    if sig_parts[0] != 'sha1' or len(sig_parts) != 2:
        # We don't know what this is.
        return HttpResponseBadRequest('Unsupported HTTP_X_HUB_SIGNATURE')

    if m.hexdigest() != sig_parts[1]:
        return HttpResponseBadRequest('Bad signature.')

        return HttpResponseBadRequest('Invalid payload format')
                                  local_site_name, repository,