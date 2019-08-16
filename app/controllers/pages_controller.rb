class PagesController < ApplicationController
	def welcome
		@greeting = "Home action says: Hello Meraki world!"
	end
end
