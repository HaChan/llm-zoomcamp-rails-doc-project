Active StorageActive Storage makes it simple to upload and reference files in cloud services likeAmazon S3,Google Cloud Storage, orMicrosoft Azure Storage, and attach those files to Active Records. Supports having one main service and mirrors in other services for redundancy. It also provides a disk service for testing or local deployments, but the focus is on cloud storage.Files can be uploaded from the server to the cloud or directly from the client to the cloud.Image files can furthermore be transformed using on-demand variants for quality, aspect ratio, size, or any otherMiniMagickorVipssupported transformation.You can read more about Active Storage in theActive Storage Overviewguide.Compared to other storage solutionsA key difference to how Active Storage works compared to other attachment solutions in Rails is through the use of built-inBlobandAttachmentmodels (backed by Active Record). This means existing application models do not need to be modified with additional columns to associate with files. Active Storage uses polymorphic associations via theAttachmentjoin model, which then connects to the actualBlob.Blobmodels store attachment metadata (filename, content-type, etc.), and their identifier key in the storage service. Blob models do not store the actual binary data. They are intended to be immutable in spirit. One file, one blob. You can associate the same blob with multiple application models as well. And if you want to do transformations of a givenBlob, the idea is that youâll simply create a new one, rather than attempt to mutate the existing one (though of course you can delete the previous version later if you donât need it).InstallationRunbin/rails active_storage:installto copy over active_storage migrations.NOTE: If the task cannot be found, verify thatrequire "active_storage/engine"is present inconfig/application.rb.ExamplesOne attachment:class User < ApplicationRecord
  # Associates an attachment and a blob. When the user is destroyed they are
  # purged by default (models destroyed, and resource files deleted).
  has_one_attached :avatar
end

# Attach an avatar to the user.
user.avatar.attach(io: File.open("/path/to/face.jpg"), filename: "face.jpg", content_type: "image/jpeg")

# Does the user have an avatar?
user.avatar.attached? # => true

# Synchronously destroy the avatar and actual resource files.
user.avatar.purge

# Destroy the associated models and actual resource files async, via Active Job.
user.avatar.purge_later

# Does the user have an avatar?
user.avatar.attached? # => false

# Generate a permanent URL for the blob that points to the application.
# Upon access, a redirect to the actual service endpoint is returned.
# This indirection decouples the public URL from the actual one, and
# allows for example mirroring attachments in different services for
# high-availability. The redirection has an HTTP expiration of 5 min.
url_for(user.avatar)

class AvatarsController < ApplicationController
  def update
    # params[:avatar] contains an ActionDispatch::Http::UploadedFile object
    Current.user.avatar.attach(params.require(:avatar))
    redirect_to Current.user
  end
endMany attachments:class Message < ApplicationRecord
  has_many_attached :images
end<%= form_with model: @message, local: true do |form| %>
  <%= form.text_field :title, placeholder: "Title" %><br>
  <%= form.text_area :content %><br><br>

  <%= form.file_field :images, multiple: true %><br>
  <%= form.submit %>
<% end %>class MessagesController < ApplicationController
  def index
    # Use the built-in with_attached_images scope to avoid N+1
    @messages = Message.all.with_attached_images
  end

  def create
    message = Message.create! params.require(:message).permit(:title, :content, images: [])
    redirect_to message
  end

  def show
    @message = Message.find(params[:id])
  end
endVariation of image attachment:<%# Hitting the variant URL will lazy transform the original blob and then redirect to its new service location %>
<%= image_tag user.avatar.variant(resize_to_limit: [100, 100]) %>Fileserving strategiesActive Storage supports two ways to serve files: redirecting and proxying.RedirectingActive Storage generates stable application URLs for files which, when accessed, redirect to signed, short-lived service URLs. This relieves application servers of the burden of serving file data. It is the default file serving strategy.When the application is configured to proxy files by default, use therails_storage_redirect_pathand_urlroute helpers to redirect instead:<%= image_tag rails_storage_redirect_path(@user.avatar) %>ProxyingOptionally, files can be proxied instead. This means that your application servers will download file data from the storage service in response to requests. This can be useful for serving files from a CDN.You can configure Active Storage to use proxying by default:# config/initializers/active_storage.rb
Rails.application.config.active_storage.resolve_model_to_route = :rails_storage_proxyOr if you want to explicitly proxy specific attachments there are URL helpers you can use in the form ofrails_storage_proxy_pathandrails_storage_proxy_url.<%= image_tag rails_storage_proxy_path(@user.avatar) %>Direct uploadsActive Storage, with its included JavaScript library, supports uploading directly from the client to the cloud.Direct upload installationInclude the Active Storage JavaScript in your application's JavaScript bundle or reference it directly.Requiring directly without bundling through the asset pipeline in the application HTML with autostart:<%= javascript_include_tag "activestorage" %>Requiring via importmap-rails without bundling through the asset pipeline in the application HTML without autostart as ESM:# config/importmap.rb
pin "@rails/activestorage", to: "activestorage.esm.js"<script type="module-shim">
  import * as ActiveStorage from "@rails/activestorage"
  ActiveStorage.start()
</script>Using the asset pipeline://= require activestorageUsing the npm package:import * as ActiveStorage from "@rails/activestorage"
ActiveStorage.start()Annotate file inputs with the direct upload URL.<%= form.file_field :attachments, multiple: true, direct_upload: true %>That's it! Uploads begin upon form submission.Direct upload JavaScript eventsEvent nameEvent targetEvent data (âevent.detail`)Descriptionâdirect-uploads:start`â<form>`NoneA form containing files for direct upload fields was submitted.âdirect-upload:initialize`â<input>`â{id, file}`Dispatched for every file after form submission.âdirect-upload:start`â<input>`â{id, file}`A direct upload is starting.âdirect-upload:before-blob-request`â<input>`â{id, file, xhr}`Before making a request to your application for direct upload metadata.âdirect-upload:before-storage-request`â<input>`â{id, file, xhr}`Before making a request to store a file.âdirect-upload:progress`â<input>`â{id, file, progress}`As requests to store files progress.âdirect-upload:error`â<input>`â{id, file, error}`An error occurred. An âalert` will display unless this event is canceled.âdirect-upload:end`â<input>`â{id, file}`A direct upload has ended.âdirect-uploads:end`â<form>`NoneAll direct uploads have ended.LicenseActive Storage is released under theMIT License.SupportAPI documentation is at:api.rubyonrails.orgBug reports for the Ruby on Rails project can be filed here:github.com/rails/rails/issuesFeature requests should be discussed on the rails-core mailing list here:discuss.rubyonrails.org/c/rubyonrails-core