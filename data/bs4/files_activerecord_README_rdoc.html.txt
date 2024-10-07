Active Record â Object-relational mapping in RailsActive Record connects classes to relational database tables to establish an almost zero-configuration persistence layer for applications. The library provides a base class that, when subclassed, sets up a mapping between the new class and an existing table in the database. In the context of an application, these classes are commonly referred to asmodels. Models can also be connected to other models; this is done by definingassociations.Active Record relies heavily on naming in that it uses class and association names to establish mappings between respective database tables and foreign key columns. Although these mappings can be defined explicitly, itâs recommended to follow naming conventions, especially when getting started with the library.You can read more about Active Record in theActive Record Basicsguide.A short rundown of some of the major features:Automated mapping between classes and tables, attributes and columns.class Product < ActiveRecord::Base
endThe Product class is automatically mapped to the table named âproductsâ, which might look like this:CREATE TABLE products (
  id bigint NOT NULL auto_increment,
  name varchar(255),
  PRIMARY KEY  (id)
);This would also define the following accessors:Product#nameandProduct#name=(new_name).Learn moreAssociations between objects defined by simple class methods.class Firm < ActiveRecord::Base
  has_many   :clients
  has_one    :account
  belongs_to :conglomerate
endLearn moreAggregations of value objects.class Account < ActiveRecord::Base
  composed_of :balance, class_name: 'Money',
              mapping: %w(balance amount)
  composed_of :address,
              mapping: [%w(address_street street), %w(address_city city)]
endLearn moreValidation rules that can differ for new or existing objects.class Account < ActiveRecord::Base
  validates :subdomain, :name, :email_address, :password, presence: true
  validates :subdomain, uniqueness: true
  validates :terms_of_service, acceptance: true, on: :create
  validates :password, :email_address, confirmation: true, on: :create
endLearn moreCallbacks available for the entire life cycle (instantiation, saving, destroying, validating, etc.).class Person < ActiveRecord::Base
  before_destroy :invalidate_payment_plan
  # the `invalidate_payment_plan` method gets called just before Person#destroy
endLearn moreInheritance hierarchies.class Company < ActiveRecord::Base; end
class Firm < Company; end
class Client < Company; end
class PriorityClient < Client; endLearn moreTransactions.# Database transaction
Account.transaction do
  david.withdrawal(100)
  mary.deposit(100)
endLearn moreReflections on columns, associations, and aggregations.reflection = Firm.reflect_on_association(:clients)
reflection.klass # => Client (class)
Firm.columns # Returns an array of column descriptors for the firms tableLearn moreDatabase abstraction through simple adapters.# connect to SQLite3
ActiveRecord::Base.establish_connection(adapter: 'sqlite3', database: 'dbfile.sqlite3')

# connect to MySQL with authentication
ActiveRecord::Base.establish_connection(
  adapter:  'mysql2',
  host:     'localhost',
  username: 'me',
  password: 'secret',
  database: 'activerecord'
)Learn moreand read about the built-in support forMySQL,PostgreSQL, andSQLite3.Logging support forLog4randLogger.ActiveRecord::Base.logger = ActiveSupport::Logger.new(STDOUT)
ActiveRecord::Base.logger = Log4r::Logger.new('Application Log')Database agnostic schema management with Migrations.class AddSystemSettings < ActiveRecord::Migration[7.2]
  def up
    create_table :system_settings do |t|
      t.string  :name
      t.string  :label
      t.text    :value
      t.string  :type
      t.integer :position
    end

    SystemSetting.create name: 'notice', label: 'Use notice?', value: 1
  end

  def down
    drop_table :system_settings
  end
endLearn morePhilosophyActive Record is an implementation of the object-relational mapping (ORM)patternby the same name described by Martin Fowler:âAn object that wraps a row in a database table or view, encapsulates the database access, and adds domain logic on that data.âActive Record attempts to provide a coherent wrapper as a solution for the inconvenience that is object-relational mapping. The prime directive for this mapping has been to minimize the amount of code needed to build a real-world domain model. This is made possible by relying on a number of conventions that make it easy for Active Record to infer complex relations and structures from a minimal amount of explicit direction.Convention over Configuration:No XML files!Lots of reflection and run-time extensionMagic is not inherently a bad wordAdmit the Database:Lets you drop down to SQL for odd cases and performanceDoesnât attempt to duplicate or replace data definitionsDownload and installationThe latest version of Active Record can be installed with RubyGems:$ gem install activerecordSource code can be downloaded as part of the Rails project on GitHub:github.com/rails/rails/tree/main/activerecordLicenseActive Record is released under the MIT license:opensource.org/licenses/MITSupportAPI documentation is at:api.rubyonrails.orgBug reports for the Ruby on Rails project can be filed here:github.com/rails/rails/issuesFeature requests should be discussed on the rails-core mailing list here:discuss.rubyonrails.org/c/rubyonrails-core