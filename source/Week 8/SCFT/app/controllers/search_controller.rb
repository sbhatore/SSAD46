class SearchController < ApplicationController
	
$ilatitude_range= 0
$ielevation_range= 0
$iradius_range= 0
$icityname = " "
  def getsearchdata


	$icityname= params[:city]
	$ilatitude_range= params[:latitude_range]
	$ielevation_range= params[:elevation_range]
	$iradius_range= params[:radius_range]
  

	@mycity = Location.find_by(City: @icityname)
	
  #If the city does not exists in database 
    	if @mycity == nil 

    		redirect_to :action => 'weather' ,:city => params[:city] ,:latitude_range => params[:latitude_range], :elevation_range => params[:elevation_range] ,:radius => params[:radius_range]
	    
	
  #If the city  exist in database 
  	else
	        #redirect_to :action => 'findSurrogateCity' , :city => params[:city]
	 
	end

  end



  def findSurrogateCity
  	
  	
  	
  	#get data from JS code of geocoder
  	@latitude_mycity = params[:latitude_mycity]
  	@longitude_mycity = params[:longitude_mycity]
	@city = $icityname
	@lat_range = $ilatitude_range
  	#@elevation_mycity = params[:elevation_mycity]

	#render :text => @lat_range	
  	#set range
  	@latitude_Range_Start = @latitude_mycity.to_f - $ilatitude_range.to_f
	@latitude_Range_End = @latitude_mycity.to_f + $ilatitude_range.to_f

	@results = Location.where('Latitude > ? AND Latitude < ?',@latitude_Range_Start,@latitude_Range_End)

	#@elevation_Range_Start = @elevation_mycity - @ielevation_range.to_f
	#@elevation_Range_End = @elevation_mycity + @ielevation_range.to_f



  end

  def weather
	  @found= params[:city]
	 # render :text => @found.inspect
	  
  end 

end
