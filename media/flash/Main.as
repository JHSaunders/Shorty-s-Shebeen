package
{
	import flash.media.*;
	import flash.geom.*
	import flash.display.*;
	import flash.events.*;
	import flash.net.*;
	import flash.system.*;
	import flash.text.*;
	import flash.filters.*;
	
	public class Main extends MovieClip {
		
		
		//main movie clip - the Flame to displace
		private var movieClip:MovieClip;
		
		//gradient base perturbation 0 perturbation on the bottom full on the top
		private var mc_gradientBasePerturbation:MovieClip;
		//The displacement map noise+gradrient
		private var bitmapDataNoise:BitmapData;

		//one point by octave in noise
		private var _offsets:Array = [new Point(), new Point(), new Point(), new Point(), new Point(), new Point()];
		
		//The animation is very sensitive to these variables
		//base to compose noise
		private var _baseX:Number;
		private var _baseY:Number;
		//scale of disturbances
		private var _scaleX:Number; 
		private var _scaleY:Number;
		//speed of the flame
		private var speed:int;
		
		//the filter apply to the flame
		private var displacementMapFilter:DisplacementMapFilter;
		
		public function Main ()
		{
			super();
			stage.quality = StageQuality.BEST;
			stage.scaleMode = StageScaleMode.NO_SCALE;
			stage.align = StageAlign.TOP_LEFT;
			
			loaderInfo.addEventListener(Event.INIT, 		initHandler);
			stage.addEventListener(Event.ENTER_FRAME, 		enterFrameHandler);
		}
		
		
		private function initHandler(event:Event=null):void
		{
			
			//Chose the movieclip you want
			movieClip = mc_flame2;
			
			//most important variables to create good result on disturbance.60/150/30/60/15. 30/70/10/10/8
			_baseX 	= 60;
			_baseY 	= 150;
			_scaleX = 10; 
			_scaleY = 10;
			speed   = 4;
			
			//init the map
			initDisplacementMapFilter();
			
			movieClip.filters = [displacementMapFilter];
			
			initGradientPerturbation();
			
			//for debug purpose
			//mc_perturbation = new MovieClip();
			//addChild(mc_perturbation);
			
		}

		
		//INIT DISPLACEMENT MAP FILTER
	  private function initDisplacementMapFilter()
	  {
  		  	bitmapDataNoise = new BitmapData(movieClip.width, movieClip.height, true, 0x00FFFFFF);
			
			  //you must test other 
			var mapBitmap:BitmapData = bitmapDataNoise;
			var mapPoint:Point = new Point(0,0);
			var componentX:uint = BitmapDataChannel.RED ; 
			var componentY:uint = BitmapDataChannel.BLUE ; 
			var _scaleX:Number = this._scaleX; 
			var _scaleY:Number = this._scaleY;
			var mode:String = DisplacementMapFilterMode.CLAMP;
			var color:uint = 0x000000;
			var _alpha:Number = 0.0;
		  
			displacementMapFilter = new DisplacementMapFilter(mapBitmap, mapPoint,componentX,componentY,_scaleX,_scaleY, mode, color, _alpha);
	  }

		
		private function initGradientPerturbation():void
		{
			mc_gradientBasePerturbation = new MovieClip();

			/** FOR debug purpose
			addChild(mc_gradientBasePerturbation);
			mc_gradientBasePerturbation.x = 700;
			mc_gradientBasePerturbation.y = 0;
			**/
			
			//mc_gradientBasePerturbation.opaqueBackground = 0xff000;

			var type:String = GradientType.LINEAR;
			var colors:Array = [0xff0080,0x800080]; 
			var alphas:Array =  [0,255];
			var ratios:Array = [0,255];
			var matrix:Matrix = new Matrix();
			var varspreadMethod:String = SpreadMethod.PAD;
			var interpolationMethod:String = InterpolationMethod.LINEAR_RGB;
			var focalPointRatio:Number = 0
 
			matrix.createGradientBox(movieClip.width, movieClip.height, Math.PI/2, 0, 0);
			
			mc_gradientBasePerturbation.graphics.beginGradientFill(type, colors, alphas, ratios, matrix, varspreadMethod, interpolationMethod, focalPointRatio);
			mc_gradientBasePerturbation.graphics.lineTo(movieClip.width, 0);
			mc_gradientBasePerturbation.graphics.lineTo(movieClip.width, movieClip.height);
			mc_gradientBasePerturbation.graphics.lineTo(0, movieClip.height);
			mc_gradientBasePerturbation.graphics.lineTo(0, 0);
			mc_gradientBasePerturbation.graphics.endFill();

		}

		////////////////////////////////////////////////////////

	  
	  //UPDATE
      private function updateBitmapNoise()
	  {
			// moves offsets within animation
			for (var i:Number = 0; i < _offsets.length; ++i){
				this._offsets[i].y += speed;
			}
			  
			  var baseX:Number 			= this._baseX;
			  var baseY:Number 			= this._baseY;
			  var numOctaves:uint 		= 3;
			  var randomSeed:int  		= 0;
			  var stitch:Boolean  		= true; 
			  var fractalNoise:Boolean 	= true;
			  var channelOptions:uint 	= BitmapDataChannel.RED | BitmapDataChannel.BLUE;
			  var grayScale:Boolean 	= false;
			  var offsets:Array 		= this._offsets;
			  
			  
			  bitmapDataNoise.perlinNoise(baseX,baseY,numOctaves,randomSeed,stitch,fractalNoise, channelOptions,grayScale,offsets);
		}

	private function updateBitmapNoiseAddBase()
	{
			var source:IBitmapDrawable;
			var matrix:Matrix = null; 
			var colorTransform:ColorTransform;
			var blendMode:String;
			var clipRect:Rectangle;
			var smoothing:Boolean;
			
			source = mc_gradientBasePerturbation;
			matrix = new Matrix();
			colorTransform = null;
			blendMode  = BlendMode.LAYER; 
			//clipRect   = new Rectangle(flameWidth, flameHeight); 
			clipRect   = null; 
			smoothing  = true;
			
			bitmapDataNoise.draw(source, matrix, colorTransform, blendMode, clipRect, smoothing);
	}


	
		private function swapFilter():void
		{
		 //SWAP FILTERS on flame
  		  var filterList;
		  var displacementMapFilter:DisplacementMapFilter;
		  
		  filterList = movieClip.filters;
		  displacementMapFilter = filterList[0];
		  displacementMapFilter.mapBitmap = bitmapDataNoise;
		  movieClip.filters = filterList;
		  
		}

		
		private function enterFrameHandler(event:Event=null):void
		{
			updateBitmapNoise();
			updateBitmapNoiseAddBase();
			swapFilter();
			
			//For debug purpose
			//perturbationDebug();
		}
		
		//For debug purpose
		/*
		private function perturbationDebug():void
		{
			mc_perturbation.x = 500;
			mc_perturbation.y = 0;
			
			var bitmap:BitmapData = bitmapDataNoise;
			var matrix:Matrix = null; 
			var repeat:Boolean = true; 
			var smooth:Boolean = false;
			
			mc_perturbation.graphics.beginBitmapFill (bitmap, matrix, repeat, smooth);
			mc_perturbation.graphics.lineTo(movieClip.width, 0);
			mc_perturbation.graphics.lineTo(movieClip.width, movieClip.height);
			mc_perturbation.graphics.lineTo(0, movieClip.height);
			mc_perturbation.graphics.lineTo(0, 0);
			mc_perturbation.graphics.endFill();
		}
		**/
		
	}
}