from GLSL_stuff import compile_program


program_Shafts = compile_program(
    """

//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();
  gl_TexCoord[0] = gl_MultiTexCoord0;
}
    """,
    """

/*FRAGMENT_SHADER*/
uniform sampler2D FullSampler;
uniform sampler2D BlurSampler;
uniform vec4 sun_pos;

const vec4 ShaftParams	= vec4(0.05, 1.0, 0.05, 1.0);
const vec4 sunColor	= vec4(0.9, 0.8, 0.6, 1.0);

float saturate(float val)
{
	return clamp(val,0.0,1.0);
}

void main(void)
{
	vec2  sunPosProj = sun_pos.xy;
	float sign = sun_pos.w;

	vec2  tc = gl_TexCoord[0].xy;

	vec2  sunVec = sunPosProj.xy - tc; // + vec2(0.5,0.5);
	float sunDist = saturate(sign) * (1.0 - saturate(dot(sunVec,sunVec) * ShaftParams.y));

	sunVec *= ShaftParams.x * sign;

	tc += sunVec;
	vec4 accum = texture2D(BlurSampler, tc);
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.875;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.75;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.625;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.5;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.375;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.25;
	tc += sunVec;
	accum += texture2D(BlurSampler, tc) * 0.125;

	accum  *= 1.65 * sunDist;

	vec4 cScreen = texture2D(FullSampler, gl_TexCoord[0].xy);
	accum = cScreen + accum * ShaftParams.w * sunColor * ( 1.0 - cScreen );

	gl_FragColor = accum;
}



""",
)


program_Combine = compile_program(
    """

//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();   // This transforms the input vertex the same way the fixed-function pipeline would
  gl_TexCoord[0] = gl_MultiTexCoord0;
}
    """,
    """
//[Pixel_Shader]
uniform sampler2D Scene;

uniform sampler2D Pass0_tex1;
uniform sampler2D Pass0_tex2;
uniform sampler2D Pass0_tex3;
uniform sampler2D Pass0_tex4;

uniform sampler2D Pass1_tex1;
uniform sampler2D Pass1_tex2;
uniform sampler2D Pass1_tex3;
uniform sampler2D Pass1_tex4;

uniform sampler2D Pass2_tex1;
uniform sampler2D Pass2_tex2;
uniform sampler2D Pass2_tex3;
uniform sampler2D Pass2_tex4;

void main(void)
{
    vec4 t0 = texture2D(Scene, gl_TexCoord[0].st);

    vec4 p0t1 = texture2D(Pass0_tex1, gl_TexCoord[0].st);
    vec4 p0t2 = texture2D(Pass0_tex2, gl_TexCoord[0].st);
    vec4 p0t3 = texture2D(Pass0_tex3, gl_TexCoord[0].st);
    vec4 p0t4 = texture2D(Pass0_tex4, gl_TexCoord[0].st);

    vec4 p1t1 = texture2D(Pass1_tex1, gl_TexCoord[0].st);
    vec4 p1t2 = texture2D(Pass1_tex2, gl_TexCoord[0].st);
    vec4 p1t3 = texture2D(Pass1_tex3, gl_TexCoord[0].st);
    vec4 p1t4 = texture2D(Pass1_tex4, gl_TexCoord[0].st);

    vec4 p2t1 = texture2D(Pass2_tex1, gl_TexCoord[0].st);
    vec4 p2t2 = texture2D(Pass2_tex2, gl_TexCoord[0].st);
    vec4 p2t3 = texture2D(Pass2_tex3, gl_TexCoord[0].st);
    vec4 p2t4 = texture2D(Pass2_tex4, gl_TexCoord[0].st);


    gl_FragColor = t0 + p0t1 + p0t2 + p0t3 + p0t4 + p1t1 + p1t2 + p1t3 + p1t4 + p2t1 + p2t2 + p2t3 + p2t4;
}

""",
)


program_ExtractBrightAreas = compile_program(
    """

//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();
  gl_TexCoord[0] = gl_MultiTexCoord0;
}
    """,
    """
//[Pixel_Shader]
uniform sampler2D source;
uniform float threshold;

void main(void)
{
    vec4 c = texture2D(source, gl_TexCoord[0].st);
    float rgb = c.r + c.g + c.b;
    if (rgb > threshold)   // threshold = 1.9
       gl_FragColor = c;
    else
       gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
}

""",
)


# shaders are taken from http://www.geeks3d.com/20091116/shader-library-2d-shockwave-post-processing-filter-glsl/
program_ShockWave = compile_program(
    """

//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();
  gl_TexCoord[0] = gl_MultiTexCoord0;
}
    """,
    """
//[Pixel_Shader]
uniform sampler2D sceneTex;     // texture unit 0
uniform vec2 center[10];        
uniform vec3 shockParams[10];   // 10.0, 0.8, 0.1
uniform float time[10];         // effect elapsed time
uniform int imax;               // how many shaders

void main()
{
  vec2 uv = gl_TexCoord[0].xy;
  vec2 texCoord = uv;
  for(int i=0; i<imax; i++)
     {
      float distance = distance(uv, center[i]);
      //if ( (distance <= (time[i] + shockParams[i].z)) && (distance >= (time[i] - shockParams[i].z)) )
      if (distance <= (time[i] + shockParams[i].z))
         if (distance >= (time[i] - shockParams[i].z))
            {
              float diff = (distance - time[i]);
              float powDiff = 1.0 - pow(abs(diff*shockParams[i].x), shockParams[i].y);
              float diffTime = diff  * powDiff;
              vec2 diffUV = normalize(uv - center[i]);
              texCoord = uv + (diffUV * diffTime);
            }
     }

   gl_FragColor = texture2D(sceneTex, texCoord);
}
""",
)

program_multitex = compile_program(
    """

//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();
  gl_TexCoord[0] = gl_MultiTexCoord0;
}
    """,
    """
uniform sampler2D Texture_0;     // texture unit 0
uniform sampler2D Texture_1;

uniform vec2 displ;

void main() {
  vec2 uv = gl_TexCoord[0].xy;
  vec2 texCoord0 = uv - displ;
  vec2 texCoord1 = uv + displ;

  vec4 color0 = texture2D(Texture_0, texCoord0);
  vec4 color1 = texture2D(Texture_1, texCoord1);
  //vec4 color3 = vec4(1.0, 1.0, 0.0, 1.0);
  vec4 tmp = mix(color0, color1, 0.5);

  //gl_FragColor = mix(tmp, color3, 0.4);
  gl_FragColor = tmp;
}
    """,
)

program_blur = compile_program(
    """
//[Vertex_Shader]
void main(void)
{
  gl_Position = ftransform();
  gl_TexCoord[0] = gl_MultiTexCoord0;
}

""",
    """

//[Pixel_Shader]
uniform sampler2D sceneTex; // 0

uniform float rt_w; // render target width
uniform float rt_h; // render target height
uniform float vx_offset;

float offset[3] = float[]( 0.0, 1.3846153846, 3.2307692308 );
float weight[3] = float[]( 0.2270270270, 0.3162162162, 0.0702702703 );

void main()
{
  vec3 tc = vec3(0.0, 0.0, 0.0);
  if (gl_TexCoord[0].x<(vx_offset-0.01))
  {
    vec2 uv = gl_TexCoord[0].xy;
    tc = texture2D(sceneTex, uv).rgb * weight[0];

    for (int i=1; i<3; i++)
    {
      tc += texture2D(sceneTex, uv + vec2(offset[i])/rt_w, 0.0).rgb * weight[i];
      tc += texture2D(sceneTex, uv - vec2(offset[i])/rt_w, 0.0).rgb * weight[i];
    }
  }
  else if (gl_TexCoord[0].x>=(vx_offset+0.01))
  {
    tc = texture2D(sceneTex, gl_TexCoord[0].xy).rgb;
  }
  gl_FragColor = vec4(tc, 1.0);
}
""",
)

"""
    {
      tc += texture2D(sceneTex, uv + vec2(offset[i])/rt_w, 0.0).rgb \
              * weight[i];
      tc += texture2D(sceneTex, uv - vec2(offset[i])/rt_w, 0.0).rgb \
              * weight[i];
    }
"""

# http://www.gamedev.ru/code/forum/?id=90743
program_light = compile_program(
    """
//[Vertex_Shader]

uniform	vec4	lightPos, eyePos;

varying vec3 l, v, n;


void main(void)
{
    vec3 p = vec3(gl_ModelViewMatrix * gl_Vertex);      // transformed point to world space

    l = normalize(vec3(lightPos) - p);                  // vector to light source
    v = normalize(vec3(eyePos)   - p);                  // vector to the eye
    n = normalize(gl_NormalMatrix * gl_Normal);         // transformed n

    gl_TexCoord[0] = gl_MultiTexCoord0;

    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
   

""",
    """

//[Pixel_Shader]

uniform sampler2D Texture_0;

varying vec3 l, v, n;


void main (void)
{
    const vec4  diffColor = vec4(1.0, 1.0, 1.0, 1.0);
    const vec4  ambientColor = vec4(0.1, 0.1, 0.1, 1.0);
    const vec4  specColor = vec4(0.7, 0.7, 0.0, 0.0);
    const float specPower = 30.0;

    vec3 n2   = normalize(n);
    vec3 l2   = normalize(l);
    vec3 v2   = normalize(v);
    vec3 r    = reflect(-v2, n2);

    vec4 diff = diffColor * max(dot(n2, l2), 0.0);
    vec4 spec = specColor * pow(max(dot(l2, r), 0.0), specPower);

    vec2 texCoord0 = gl_TexCoord[0].xy;
    vec4 texColor0 = texture2D(Texture_0, texCoord0);

    gl_FragColor = (diff + ambientColor) * texColor0;
}
       
    """,
)


# glLib Particles system
PARTICLE_UPDATE_program = compile_program(
    """
//[Vertex_Shader]

uniform sampler2D tex2D_1, tex2D_2, tex2D_3;

uniform float size, step;
uniform vec3 initialspeed, initalpos, scale, forces, jitter;

varying vec2 coord;
varying vec4 vertex;

void main()
{   vertex         = gl_Vertex;
    gl_TexCoord[0] = gl_MultiTexCoord0;
    
    coord = vec2(vertex.xy * vec2(1.0-(1.0/size))) + vec2(0.5/size);
    //coord = vec2(vertex.xy * vec2(1.0-(1.0/size)));
          
    vertex.xy = vec2(vertex.xy * (size-1.0)) + vec2(0.5);
    //vertex.xy = vec2(vertex.xy * (size-1.0));                     

    gl_Position = gl_ModelViewProjectionMatrix * vertex;
}

""",
    """

//[Pixel_Shader]

uniform sampler2D tex2D_1, tex2D_2, tex2D_3;
// self.pos_time_texture, self.velocity_texture, self.rand_tex.texture

uniform float size, step;
uniform vec3 initialspeed, initalpos, scale, forces, jitter;

varying vec4 vertex;
varying vec2 coord;

vec4 color, color2;

void main()
{
    vec2 uv = gl_TexCoord[0].st;
    
    vec4 pos_time        = texture2D(tex2D_1, coord);
    vec4 velocity_sample = texture2D(tex2D_2, coord);

    vec3 direction = vec3(velocity_sample.xyz - vec3(0.5)) * 2.0; //???

    float speed   = velocity_sample.w;
    vec3 velocity = speed * direction;

    pos_time.w += step;

    if(pos_time.w >= 1.0)
      {
       velocity     = initialspeed + vec3(jitter * vec3(texture2D(tex2D_3, coord).xyz - vec3(0.5)));
       pos_time.xyz = initalpos + vec3(0.5);
       pos_time.w   = 0.0;
      }

    velocity     += forces;
    pos_time.xyz += velocity;

    float new_speed = length(velocity);

    color  = pos_time;
    color2 = vec4(vec3(normalize(velocity.xyz) * 0.5) + vec3(0.5), new_speed);

    color  = clamp(color,  0.0, 1.0);
    color2 = clamp(color2, 0.0, 1.0);

    gl_FragData[0] = color;
    gl_FragData[1] = color2;
}
    """,
)


# glLib Particles system
PARTICLE_DRAW_program = compile_program(
    """
//[Vertex_Shader]

uniform sampler2D tex2D_1,tex2D_2;

uniform float size, fade, point_size;
uniform vec3 trans, scale;

varying vec4 vertex;
varying float continuing;
varying float intensity;


void main()
{
    gl_TexCoord[0] = gl_MultiTexCoord0;
    vertex = gl_Vertex;

    vec2 coord    = vec2(vertex.xy * vec2(1.0-(1.0/size))) + vec2(0.5/size);
    vec4 pos_time = texture2D(tex2D_1, coord);

    intensity = 1.0 - pow(pos_time.w, fade);

    vertex.xyz = pos_time.xyz - vec3(0.5);
    vertex     = vec4(vec3(vertex.xyz * scale * 2.0) + trans,1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vertex;
    continuing  = 0.0;

    gl_PointSize = point_size/length(gl_Position);
    continuing = clamp(floor(gl_PointSize), 0.0, 1.0);
}

""",
    """

//[Pixel_Shader]
uniform sampler2D tex2D_1,tex2D_2;

uniform float size, fade, point_size;
uniform vec3 trans, scale;

varying vec4 vertex;
varying float continuing;
varying float intensity;

vec4 color;

void main()
{
    vec2 uv = gl_TexCoord[0].st;
    
    vec2 v_rot = normalize(vertex.zw);
    vec4 l_uv = vec4(0.0, 0.0, gl_PointCoord.xy);

    l_uv.zw -= vec2(0.5, 0.5);

    l_uv.x = l_uv.z*v_rot.x;
    l_uv.y = l_uv.w*v_rot.x;
    l_uv.x -= l_uv.w*v_rot.y;
    l_uv.y += l_uv.z*v_rot.y;

    color    = texture2D(tex2D_2,l_uv.xy + vec2(0.5, 0.5));
    color.a *= intensity*continuing;
    color    = clamp(color, 0.0, 1.0);

    gl_FragData[0] = color;
}
    """,
)
