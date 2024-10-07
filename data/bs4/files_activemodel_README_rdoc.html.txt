Active Model â model interfaces for RailsActive Model provides a known set of interfaces for usage in model classes. They allow for Action Pack helpers to interact with non-Active Record models, for example. Active Model also helps with building custom ORMs for use outside of the Rails framework.You can read more about Active Model in theActive Model Basicsguide.Prior to Rails 3.0, if a plugin or gem developer wanted to have an object interact with Action Pack helpers, it was required to either copy chunks of code from Rails, or monkey patch entire helpers to make them handle objects that did not exactly conform to the Active Record interface. This would result in code duplication and fragile applications that broke on upgrades. Active Model solves this by defining an explicit API. You can read more about the API inActiveModel::Lint::Tests.Active Model provides a default module that implements the basic API required to integrate with Action Pack out of the box:ActiveModel::API.class Person
  include ActiveModel::API

  attr_accessor :name, :age
  validates_presence_of :name
end

person = Person.new(name: 'bob', age: '18')
person.name   # => 'bob'
person.age    # => '18'
person.valid? # => trueIt includes model name introspections, conversions, translations and validations, resulting in a class suitable to be used with Action Pack. SeeActiveModel::APIfor more examples.Active Model also provides the following functionality to have ORM-like behavior out of the box:Add attribute magic to objectsclass Person
  include ActiveModel::AttributeMethods

  attribute_method_prefix 'clear_'
  define_attribute_methods :name, :age

  attr_accessor :name, :age

  def clear_attribute(attr)
    send("#{attr}=", nil)
  end
end

person = Person.new
person.clear_name
person.clear_ageLearn moreCallbacks for certain operationsclass Person
  extend ActiveModel::Callbacks
  define_model_callbacks :create

  def create
    run_callbacks :create do
      # Your create action methods here
    end
  end
endThis generatesbefore_create,around_createandafter_createclass methods that wrap your create method.Learn moreTracking value changesclass Person
  include ActiveModel::Dirty

  define_attribute_methods :name

  def name
    @name
  end

  def name=(val)
    name_will_change! unless val == @name
    @name = val
  end

  def save
    # do persistence work
    changes_applied
  end
end

person = Person.new
person.name             # => nil
person.changed?         # => false
person.name = 'bob'
person.changed?         # => true
person.changed          # => ['name']
person.changes          # => { 'name' => [nil, 'bob'] }
person.save
person.name = 'robert'
person.save
person.previous_changes # => {'name' => ['bob, 'robert']}Learn moreAddingerrorsinterface to objectsExposing error messages allows objects to interact with Action Pack helpers seamlessly.class Person

  def initialize
    @errors = ActiveModel::Errors.new(self)
  end

  attr_accessor :name
  attr_reader   :errors

  def validate!
    errors.add(:name, "cannot be nil") if name.nil?
  end

  def self.human_attribute_name(attr, options = {})
    "Name"
  end
end

person = Person.new
person.name = nil
person.validate!
person.errors.full_messages
# => ["Name cannot be nil"]Learn moreModel name introspectionclass NamedPerson
  extend ActiveModel::Naming
end

NamedPerson.model_name.name   # => "NamedPerson"
NamedPerson.model_name.human  # => "Named person"Learn moreMaking objects serializableActiveModel::Serializationprovides a standard interface for your object to provideto_jsonserialization.class SerialPerson
  include ActiveModel::Serialization

  attr_accessor :name

  def attributes
    {'name' => name}
  end
end

s = SerialPerson.new
s.serializable_hash   # => {"name"=>nil}

class SerialPerson
  include ActiveModel::Serializers::JSON
end

s = SerialPerson.new
s.to_json             # => "{\"name\":null}"Learn moreInternationalization (i18n) supportclass Person
  extend ActiveModel::Translation
end

Person.human_attribute_name('my_attribute')
# => "My attribute"Learn moreValidation supportclass Person
  include ActiveModel::Validations

  attr_accessor :first_name, :last_name

  validates_each :first_name, :last_name do |record, attr, value|
    record.errors.add attr, "starts with z." if value.start_with?("z")
  end
end

person = Person.new
person.first_name = 'zoolander'
person.valid?  # => falseLearn moreCustom validatorsclass HasNameValidator < ActiveModel::Validator
  def validate(record)
    record.errors.add(:name, "must exist") if record.name.blank?
  end
end

class ValidatorPerson
  include ActiveModel::Validations
  validates_with HasNameValidator
  attr_accessor :name
end

p = ValidatorPerson.new
p.valid?                  # =>  false
p.errors.full_messages    # => ["Name must exist"]
p.name = "Bob"
p.valid?                  # =>  trueLearn moreDownload and installationThe latest version of Active Model can be installed with RubyGems:$ gem install activemodelSource code can be downloaded as part of the Rails project on GitHubgithub.com/rails/rails/tree/main/activemodelLicenseActive Model is released under the MIT license:opensource.org/licenses/MITSupportAPI documentation is at:api.rubyonrails.orgBug reports for the Ruby on Rails project can be filed here:github.com/rails/rails/issuesFeature requests should be discussed on the rails-core mailing list here:discuss.rubyonrails.org/c/rubyonrails-core