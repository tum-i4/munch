/* sleep - delay for a specified amount of time.
   Copyright (C) 84, 1991-1997, 1999-2005, 2007 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <config.h>
#include <stdio.h>
#include <sys/types.h>
#include <getopt.h>

#include "system.h"
#include "c-strtod.h"
#include "error.h"
#include "long-options.h"
#include "quote.h"
#include "xnanosleep.h"
#include "xstrtod.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "sleep"

#define AUTHORS "Jim Meyering", "Paul Eggert"

/* The name by which this program was run. */
char *program_name;

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("\
Usage: %s NUMBER[SUFFIX]...\n\
  or:  %s OPTION\n\
Pause for NUMBER seconds.  SUFFIX may be `s' for seconds (the default),\n\
`m' for minutes, `h' for hours or `d' for days.  Unlike most implementations\n\
that require NUMBER be an integer, here NUMBER may be an arbitrary floating\n\
point number.  Given two or more arguments, pause for the amount of time\n\
specified by the sum of their values.\n\
\n\
"),
	      program_name, program_name);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

/* Given a floating point value *X, and a suffix character, SUFFIX_CHAR,
   scale *X by the multiplier implied by SUFFIX_CHAR.  SUFFIX_CHAR may
   be the NUL byte or `s' to denote seconds, `m' for minutes, `h' for
   hours, or `d' for days.  If SUFFIX_CHAR is invalid, don't modify *X
   and return false.  Otherwise return true.  */

static bool
apply_suffix (double *x, char suffix_char)
{
  int multiplier;

  switch (suffix_char)
    {
    case 0:
    case 's':
      multiplier = 1;
      break;
    case 'm':
      multiplier = 60;
      break;
    case 'h':
      multiplier = 60 * 60;
      break;
    case 'd':
      multiplier = 60 * 60 * 24;
      break;
    default:
      return false;
    }

  *x *= multiplier;

  return true;
}

/* reads input from stdin */
#define SIZE 99999

#undef initialize_main
void initialize_main(int *argc, char ***argv)
{
  char str[SIZE];
  char *iargv[SIZE];
  int  iargc;
  char temp[SIZE] = {'\0'};
  char *env;
  char env_var[SIZE] = {'\0'};
  int quotes = 0;
  int len = 0;
  int env_var_size = 0;
  int pos = 0;
  int i = 0;
  int env_flag = 0;

  if (fgets (str, SIZE, stdin) == NULL )
  {
    perror("Error while reading from stdin.");
    exit(EXIT_FAILURE);
  }

  iargv[0] = (*argv)[0];
  iargc = 1;

  len = strlen(str);
  for(i = 0; i < len; i++)
  {
    if(str[i] == ' ' || str[i] == '\t' || str[i] == '\n' || str[i] == '\r')
    {
      if(env_flag)
      {
        env_flag = 0;
        env_var[env_var_size] = '\0';
        if(strlen(env_var) == 1)
            temp[pos++] = '$';
        else
        {
          env = getenv(&env_var[1]);
          if(env != NULL)
          {
              strncpy(&temp[pos], env, strlen(env));
              pos += strlen(env);
          }
        }
        env_var[0] = '\0';
        env_var_size = 0;
        }
        if(quotes == 0)
        {
          if(strlen(temp) > 0)
          {
            temp[pos] = '\0';
            iargv[iargc] = (char *) malloc(pos);
            if(iargv[iargc] == NULL)
            {
              perror("Error while allocating memory.");
              exit(EXIT_FAILURE);
            }
            strncpy(iargv[iargc++], temp, pos);
            temp[0] = '\0';
            pos = 0;
          }
        }
        else
          temp[pos++] = str[i];
    }
    else if(str[i] == '"' || str[i] == '\'')
    {
      if(quotes == 0)
        quotes++;
      else
      {
        quotes--;
        if(env_flag)
        {
          env_flag = 0;
          env_var[env_var_size] = '\0';
          if(strlen(env_var) == 1)
          {
            temp[pos++] = '$';
          }
          else
          {
            env = getenv(&env_var[1]);
            if(env != NULL)
            {
              strncpy(&temp[pos], env, strlen(env));
              pos += strlen(env);
            }
          }
          env_var[0] = '\0';
          env_var_size = 0;
        }
        if(strlen(temp) > 0)
        {
          temp[pos] = '\0';
          iargv[iargc] = (char *) malloc(pos);
          strncpy(iargv[iargc++], temp, pos);
          temp[0] = '\0';
          pos = 0;
        }
      }
    }
    else if(str[i] == '$')
    {
      env_flag = 1;
      env_var[env_var_size++] = str[i];
    }
    else
    {
      if(env_flag)
        env_var[env_var_size++] = str[i];
      else
        temp[pos++] = str[i];
    }
  }

  *argc = iargc;
  *argv = iargv;
}

int
main (int argc, char **argv)
{
  int i;
  double seconds = 0.0;
  bool ok = true;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  parse_long_options (argc, argv, PROGRAM_NAME, PACKAGE_NAME, VERSION,
		      usage, AUTHORS, (char const *) NULL);
  if (getopt_long (argc, argv, "", NULL, NULL) != -1)
    usage (EXIT_FAILURE);

  if (argc == 1)
    {
      error (0, 0, _("missing operand"));
      usage (EXIT_FAILURE);
    }

  for (i = optind; i < argc; i++)
    {
      double s;
      const char *p;
      if (! xstrtod (argv[i], &p, &s, c_strtod)
	  /* Nonnegative interval.  */
	  || ! (0 <= s)
	  /* No extra chars after the number and an optional s,m,h,d char.  */
	  || (*p && *(p+1))
	  /* Check any suffix char and update S based on the suffix.  */
	  || ! apply_suffix (&s, *p))
	{
	  error (0, 0, _("invalid time interval %s"), quote (argv[i]));
	  ok = false;
	}

      seconds += s;
    }

  if (!ok)
    usage (EXIT_FAILURE);

  if (xnanosleep (seconds))
    error (EXIT_FAILURE, errno, _("cannot read realtime clock"));

  exit (EXIT_SUCCESS);
}
